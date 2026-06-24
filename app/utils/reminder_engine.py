"""
Reminder Engine
===============
Evaluates the 14 reminder rules from the Order Monitoring Reminders spec
and upserts / deletes rows in the `reminders` table.

Call ``regenerate_all(db)`` from the router or from any other router
after a relevant write operation.

Reminders 1-11  → "immediate":  activation_date = date.today()
Reminders 12-14 → "date-based": activation_date = a calculated date
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Dict, Optional, Tuple

from sqlalchemy.orm import Session

from app.models.order_detail import OrderDetail
from app.models.performance_guarantee import PerformanceGuarantee
from app.models.material_performance_guarantee import MaterialPerformanceGuarantee
from app.models.tendering_companies import TenderingCompanies
from app.models.lot_monitoring import LotMonitoring
from app.models.delivery_procedure import DeliveryProcedure
from app.models.tender import Tender
from app.models.reminder import ReminderTypeEnum

from app.cruds.reminder import upsert_reminder, delete_reminders_by_source


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _po_for_order(db: Session, order_id: int) -> Tuple[Optional[str], Optional[int]]:
    """Return (po_number, order_id) for an order, or (None, None)."""
    o = db.query(OrderDetail).filter(OrderDetail.order_id == order_id).first()
    if o:
        return o.po_number, o.order_id
    return None, None


def _po_for_lot(db: Session, lot_id: int) -> Tuple[Optional[str], Optional[int]]:
    """Walk lot → order to resolve po_number."""
    lot = db.query(LotMonitoring).filter(LotMonitoring.lot_id == lot_id).first()
    if lot and lot.order_id:
        return _po_for_order(db, lot.order_id)
    return None, None


def _po_for_dp(db: Session, dp_id: int) -> Tuple[Optional[str], Optional[int]]:
    """Walk delivery_procedure → lot → order to resolve po_number."""
    dp = db.query(DeliveryProcedure).filter(DeliveryProcedure.dp_id == dp_id).first()
    if dp:
        return _po_for_lot(db, dp.lot_id)
    return None, None


def _po_for_tender(db: Session, tender_id: int) -> Tuple[str, Optional[int]]:
    """
    Try to find a PO linked to this tender.
    Falls back to Tender No if no PO exists yet.
    """
    order = (
        db.query(OrderDetail)
        .filter(OrderDetail.tender_id == tender_id)
        .first()
    )
    if order:
        return order.po_number, order.order_id

    tender = db.query(Tender).filter(Tender.tender_id == tender_id).first()
    return (tender.tender_no if tender else f"Tender #{tender_id}"), None


# ─────────────────────────────────────────────
# Rule evaluators (one function per reminder)
# ─────────────────────────────────────────────

def _rule_01_tbg_to_be_issued(db: Session, stats: Dict):
    """
    1. "TBG to be issued for {PO}"
       Trigger: tender_receipt_no is entered in tendering_companies
       Condition still open: tbg_no IS NULL AND credit_card_payment_ref IS NULL
    """
    rows = (
        db.query(TenderingCompanies)
        .filter(
            TenderingCompanies.tender_receipt_no.isnot(None),
            TenderingCompanies.tbg_no.is_(None),
            TenderingCompanies.credit_card_payment_ref.is_(None),
        )
        .all()
    )
    seen = set()
    for tc in rows:
        po, oid = _po_for_tender(db, tc.tender_id)
        key = (ReminderTypeEnum.TBG_TO_BE_ISSUED, "tendering_companies", tc.tendering_companies_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.TBG_TO_BE_ISSUED,
            source_table="tendering_companies",
            source_id=tc.tendering_companies_id,
            po_number=po,
            description=f"TBG to be issued for {po}",
            activation_date=date.today(),
            order_id=oid,
        )
        stats["created"] += 1

    # Clean up reminders whose condition no longer holds
    _cleanup(db, ReminderTypeEnum.TBG_TO_BE_ISSUED, "tendering_companies", seen, stats)


def _rule_02_pbg_to_be_issued(db: Session, stats: Dict):
    """
    2. "PBG to be issued for {PO}"
       Trigger: order_date is entered (always present once order exists)
       Condition still open: no PBG row for this order, or PBG pending_status = 'NOT Issued'
    """
    orders = db.query(OrderDetail).filter(OrderDetail.order_date.isnot(None)).all()
    seen = set()
    for o in orders:
        pg = (
            db.query(PerformanceGuarantee)
            .filter(PerformanceGuarantee.order_id == o.order_id)
            .first()
        )
        # Reminder needed if no PBG exists, or PBG still "NOT Issued"
        if pg and pg.pending_status.value != "NOT Issued":
            continue

        key = (ReminderTypeEnum.PBG_TO_BE_ISSUED, "order_details", o.order_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.PBG_TO_BE_ISSUED,
            source_table="order_details",
            source_id=o.order_id,
            po_number=o.po_number,
            description=f"PBG to be issued for {o.po_number}",
            activation_date=date.today(),
            order_id=o.order_id,
        )
        stats["created"] += 1

    _cleanup(db, ReminderTypeEnum.PBG_TO_BE_ISSUED, "order_details", seen, stats)


def _rule_03_tbg_to_be_released(db: Session, stats: Dict):
    """
    3. "TBG to be released for {PO}"
       Trigger: PBG submitted_date is entered (pg_submitted_date in performance_guarantees)
       Condition still open: TBG for the same tender is not released
    """
    pgs = (
        db.query(PerformanceGuarantee)
        .filter(PerformanceGuarantee.pg_submitted_date.isnot(None))
        .all()
    )
    seen = set()
    for pg in pgs:
        order = db.query(OrderDetail).filter(OrderDetail.order_id == pg.order_id).first()
        if not order:
            continue

        # Find TBG through tender
        tc = (
            db.query(TenderingCompanies)
            .filter(TenderingCompanies.tender_id == order.tender_id)
            .first()
        )
        if not tc:
            continue

        # TBG already released? (both DEWA and bank dates filled)
        if tc.tbg_release_date_dewa and tc.tbg_release_date_bank:
            continue

        key = (ReminderTypeEnum.TBG_TO_BE_RELEASED, "performance_guarantees", pg.pg_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.TBG_TO_BE_RELEASED,
            source_table="performance_guarantees",
            source_id=pg.pg_id,
            po_number=order.po_number,
            description=f"TBG to be released for {order.po_number}",
            activation_date=date.today(),
            order_id=order.order_id,
        )
        stats["created"] += 1

    _cleanup(db, ReminderTypeEnum.TBG_TO_BE_RELEASED, "performance_guarantees", seen, stats)


def _rule_04_mpg_to_be_issued(db: Session, stats: Dict):
    """
    4. "MPG to be issued for {PO}"
       Trigger: actual_last_delivery is entered in order_details
       Condition still open: no MPG row for this order, or MPG pending_status = 'NOT Issued'
    """
    orders = (
        db.query(OrderDetail)
        .filter(OrderDetail.actual_last_delivery.isnot(None))
        .all()
    )
    seen = set()
    for o in orders:
        mpg = (
            db.query(MaterialPerformanceGuarantee)
            .filter(MaterialPerformanceGuarantee.order_id == o.order_id)
            .first()
        )
        if mpg and mpg.pending_status.value != "NOT Issued":
            continue

        key = (ReminderTypeEnum.MPG_TO_BE_ISSUED, "order_details", o.order_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.MPG_TO_BE_ISSUED,
            source_table="order_details",
            source_id=o.order_id,
            po_number=o.po_number,
            description=f"MPG to be issued for {o.po_number}",
            activation_date=date.today(),
            order_id=o.order_id,
        )
        stats["created"] += 1

    _cleanup(db, ReminderTypeEnum.MPG_TO_BE_ISSUED, "order_details", seen, stats)


def _rule_05_pbg_to_be_released(db: Session, stats: Dict):
    """
    5. "PBG to be released for {PO}"
       Trigger: MPG submitted_date is entered (mpg_submitted_date)
       Condition still open: PBG for same order not released
    """
    mpgs = (
        db.query(MaterialPerformanceGuarantee)
        .filter(MaterialPerformanceGuarantee.mpg_submitted_date.isnot(None))
        .all()
    )
    seen = set()
    for mpg in mpgs:
        pg = (
            db.query(PerformanceGuarantee)
            .filter(PerformanceGuarantee.order_id == mpg.order_id)
            .first()
        )
        if pg and pg.pending_status.value == "Released":
            continue

        po, oid = _po_for_order(db, mpg.order_id)
        if not po:
            continue

        key = (ReminderTypeEnum.PBG_TO_BE_RELEASED, "material_performance_guarantees", mpg.mpg_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.PBG_TO_BE_RELEASED,
            source_table="material_performance_guarantees",
            source_id=mpg.mpg_id,
            po_number=po,
            description=f"PBG to be released for {po}",
            activation_date=date.today(),
            order_id=oid,
        )
        stats["created"] += 1

    _cleanup(db, ReminderTypeEnum.PBG_TO_BE_RELEASED, "material_performance_guarantees", seen, stats)


def _rule_06_get_etd(db: Session, stats: Dict):
    """
    6. "Get ETD for {PO}"
       Trigger: dispatch_clearance_date entered in lot_monitoring
       Condition still open: etd_date IS NULL
    """
    lots = (
        db.query(LotMonitoring)
        .filter(
            LotMonitoring.dispatch_clearance_date.isnot(None),
            LotMonitoring.etd_date.is_(None),
        )
        .all()
    )
    seen = set()
    for lot in lots:
        po, oid = _po_for_order(db, lot.order_id)
        if not po:
            continue

        key = (ReminderTypeEnum.GET_ETD, "lot_monitoring", lot.lot_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.GET_ETD,
            source_table="lot_monitoring",
            source_id=lot.lot_id,
            po_number=po,
            description=f"Get ETD for {po}",
            activation_date=date.today(),
            order_id=oid,
        )
        stats["created"] += 1

    _cleanup(db, ReminderTypeEnum.GET_ETD, "lot_monitoring", seen, stats)


def _rule_07_get_customs_exemption(db: Session, stats: Dict):
    """
    7. "Get Customs Exemption, B/L Stamped and Authorization Letter for {PO}"
       Trigger: document_status >= 1 (Partial or All received) in delivery_procedures
    """
    dps = (
        db.query(DeliveryProcedure)
        .filter(DeliveryProcedure.document_status >= 1)
        .all()
    )
    seen = set()
    for dp in dps:
        po, oid = _po_for_dp(db, dp.dp_id)
        if not po:
            continue

        key = (ReminderTypeEnum.GET_CUSTOMS_EXEMPTION, "delivery_procedures", dp.dp_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.GET_CUSTOMS_EXEMPTION,
            source_table="delivery_procedures",
            source_id=dp.dp_id,
            po_number=po,
            description=f"Get Customs Exemption, B/L Stamped and Authorization Letter for {po}",
            activation_date=date.today(),
            order_id=oid,
        )
        stats["created"] += 1

    _cleanup(db, ReminderTypeEnum.GET_CUSTOMS_EXEMPTION, "delivery_procedures", seen, stats)


def _rule_08_prepare_asn(db: Session, stats: Dict):
    """
    8. "Prepare ASN for {PO}"
       Trigger: documents_to_agent_date entered in delivery_procedures
    """
    dps = (
        db.query(DeliveryProcedure)
        .filter(DeliveryProcedure.documents_to_agent_date.isnot(None))
        .all()
    )
    seen = set()
    for dp in dps:
        po, oid = _po_for_dp(db, dp.dp_id)
        if not po:
            continue

        key = (ReminderTypeEnum.PREPARE_ASN, "delivery_procedures", dp.dp_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.PREPARE_ASN,
            source_table="delivery_procedures",
            source_id=dp.dp_id,
            po_number=po,
            description=f"Prepare ASN for {po}",
            activation_date=date.today(),
            order_id=oid,
        )
        stats["created"] += 1

    _cleanup(db, ReminderTypeEnum.PREPARE_ASN, "delivery_procedures", seen, stats)


def _rule_09_create_delivery_note(db: Session, stats: Dict):
    """
    9. "Create Delivery Note and Gate Pass for {PO}"
       Trigger: delivery_intimation_date entered in delivery_procedures
    """
    dps = (
        db.query(DeliveryProcedure)
        .filter(DeliveryProcedure.delivery_intimation_date.isnot(None))
        .all()
    )
    seen = set()
    for dp in dps:
        po, oid = _po_for_dp(db, dp.dp_id)
        if not po:
            continue

        key = (ReminderTypeEnum.CREATE_DELIVERY_NOTE, "delivery_procedures", dp.dp_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.CREATE_DELIVERY_NOTE,
            source_table="delivery_procedures",
            source_id=dp.dp_id,
            po_number=po,
            description=f"Create Delivery Note and Gate Pass for {po}",
            activation_date=date.today(),
            order_id=oid,
        )
        stats["created"] += 1

    _cleanup(db, ReminderTypeEnum.CREATE_DELIVERY_NOTE, "delivery_procedures", seen, stats)


def _rule_10_payment_application(db: Session, stats: Dict):
    """
    10. "Payment Application for {PO}"
        Trigger: actual_delivery_date entered in lot_monitoring
    """
    lots = (
        db.query(LotMonitoring)
        .filter(LotMonitoring.actual_delivery_date.isnot(None))
        .all()
    )
    seen = set()
    for lot in lots:
        po, oid = _po_for_order(db, lot.order_id)
        if not po:
            continue

        key = (ReminderTypeEnum.PAYMENT_APPLICATION, "lot_monitoring", lot.lot_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.PAYMENT_APPLICATION,
            source_table="lot_monitoring",
            source_id=lot.lot_id,
            po_number=po,
            description=f"Payment Application for {po}",
            activation_date=date.today(),
            order_id=oid,
        )
        stats["created"] += 1

    _cleanup(db, ReminderTypeEnum.PAYMENT_APPLICATION, "lot_monitoring", seen, stats)


def _rule_11_prepare_ld_statement(db: Session, stats: Dict):
    """
    11. "Prepare LD statement for {PO}"
        Trigger: actual_last_delivery entered in order_details
    """
    orders = (
        db.query(OrderDetail)
        .filter(OrderDetail.actual_last_delivery.isnot(None))
        .all()
    )
    seen = set()
    for o in orders:
        key = (ReminderTypeEnum.PREPARE_LD_STATEMENT, "order_details", o.order_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.PREPARE_LD_STATEMENT,
            source_table="order_details",
            source_id=o.order_id,
            po_number=o.po_number,
            description=f"Prepare LD statement for {o.po_number}",
            activation_date=date.today(),
            order_id=o.order_id,
        )
        stats["created"] += 1

    _cleanup(db, ReminderTypeEnum.PREPARE_LD_STATEMENT, "order_details", seen, stats)


# ── Date-based reminders ────────────────────

def _rule_12_mpg_to_be_released(db: Session, stats: Dict):
    """
    12. "MPG to be released for {PO}"
        activation_date = mpg_expiry_date
        Condition: mpg_expiry_date set AND pending_status != 'Released'
    """
    mpgs = (
        db.query(MaterialPerformanceGuarantee)
        .filter(
            MaterialPerformanceGuarantee.mpg_expiry_date.isnot(None),
            MaterialPerformanceGuarantee.pending_status != "Released",
        )
        .all()
    )
    seen = set()
    for mpg in mpgs:
        po, oid = _po_for_order(db, mpg.order_id)
        if not po:
            continue

        key = (ReminderTypeEnum.MPG_TO_BE_RELEASED, "material_performance_guarantees", mpg.mpg_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.MPG_TO_BE_RELEASED,
            source_table="material_performance_guarantees",
            source_id=mpg.mpg_id,
            po_number=po,
            description=f"MPG to be released for {po}",
            activation_date=mpg.mpg_expiry_date,
            order_id=oid,
        )
        stats["created"] += 1

    _cleanup(db, ReminderTypeEnum.MPG_TO_BE_RELEASED, "material_performance_guarantees", seen, stats)


def _rule_13_inspection_application(db: Session, stats: Dict):
    """
    13. "Inspection Application due for Consignment for {PO}"
        activation_date = contractual_delivery_date − 75 days
        Condition: contractual_delivery_date is set
    """
    lots = (
        db.query(LotMonitoring)
        .filter(LotMonitoring.contractual_delivery_date.isnot(None))
        .all()
    )
    seen = set()
    for lot in lots:
        po, oid = _po_for_order(db, lot.order_id)
        if not po:
            continue

        activation = lot.contractual_delivery_date - timedelta(days=75)

        key = (ReminderTypeEnum.INSPECTION_APPLICATION, "lot_monitoring", lot.lot_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.INSPECTION_APPLICATION,
            source_table="lot_monitoring",
            source_id=lot.lot_id,
            po_number=po,
            description=f"Inspection Application due for Consignment for {po}",
            activation_date=activation,
            order_id=oid,
        )
        stats["created"] += 1

    _cleanup(db, ReminderTypeEnum.INSPECTION_APPLICATION, "lot_monitoring", seen, stats)


def _rule_14_get_shipping_documents(db: Session, stats: Dict):
    """
    14. "Get Shipping Documents for {PO}"
        activation_date = etd_date
        Condition: etd_date is set
    """
    lots = (
        db.query(LotMonitoring)
        .filter(LotMonitoring.etd_date.isnot(None))
        .all()
    )
    seen = set()
    for lot in lots:
        po, oid = _po_for_order(db, lot.order_id)
        if not po:
            continue

        key = (ReminderTypeEnum.GET_SHIPPING_DOCUMENTS, "lot_monitoring", lot.lot_id)
        seen.add(key)
        upsert_reminder(
            db,
            reminder_type=ReminderTypeEnum.GET_SHIPPING_DOCUMENTS,
            source_table="lot_monitoring",
            source_id=lot.lot_id,
            po_number=po,
            description=f"Get Shipping Documents for {po}",
            activation_date=lot.etd_date,
            order_id=oid,
        )
        stats["created"] += 1

    _cleanup(db, ReminderTypeEnum.GET_SHIPPING_DOCUMENTS, "lot_monitoring", seen, stats)


# ─────────────────────────────────────────────
# Cleanup helper
# ─────────────────────────────────────────────

def _cleanup(
    db: Session,
    reminder_type: ReminderTypeEnum,
    source_table: str,
    seen_keys: set,
    stats: Dict,
):
    """
    Delete reminders of this type+table whose source_id was NOT
    in the current evaluation pass (condition no longer holds).
    """
    from app.models.reminder import Reminder

    existing = (
        db.query(Reminder)
        .filter(
            Reminder.reminder_type == reminder_type,
            Reminder.source_table == source_table,
        )
        .all()
    )
    for r in existing:
        key = (reminder_type, source_table, r.source_id)
        if key not in seen_keys:
            db.delete(r)
            stats["deleted"] += 1
    db.commit()


# ─────────────────────────────────────────────
# Helper: count active reminders
# ─────────────────────────────────────────────

def _count_active(db: Session) -> int:
    from app.models.reminder import Reminder
    today = date.today()
    return (
        db.query(Reminder)
        .filter(Reminder.activation_date <= today, Reminder.is_dismissed == False)
        .count()
    )


def _finish(db: Session, stats: Dict) -> Dict[str, int]:
    stats["total_active"] = _count_active(db)
    return stats


# ─────────────────────────────────────────────
# Targeted entry points (one per source table)
# ─────────────────────────────────────────────
# Call these from the matching router so only
# the relevant rules run — not the whole DB.

def regenerate_for_tendering_companies(db: Session) -> Dict[str, int]:
    """After saving tendering_companies → rule 1 only."""
    stats: Dict[str, int] = {"created": 0, "deleted": 0}
    _rule_01_tbg_to_be_issued(db, stats)
    return _finish(db, stats)


def regenerate_for_order_details(db: Session) -> Dict[str, int]:
    """After saving order_details → rules 2, 4, 11."""
    stats: Dict[str, int] = {"created": 0, "deleted": 0}
    _rule_02_pbg_to_be_issued(db, stats)
    _rule_04_mpg_to_be_issued(db, stats)
    _rule_11_prepare_ld_statement(db, stats)
    return _finish(db, stats)


def regenerate_for_performance_guarantee(db: Session) -> Dict[str, int]:
    """After saving performance_guarantees → rule 3."""
    stats: Dict[str, int] = {"created": 0, "deleted": 0}
    _rule_03_tbg_to_be_released(db, stats)
    return _finish(db, stats)


def regenerate_for_material_performance_guarantee(db: Session) -> Dict[str, int]:
    """After saving material_performance_guarantees → rules 5, 12."""
    stats: Dict[str, int] = {"created": 0, "deleted": 0}
    _rule_05_pbg_to_be_released(db, stats)
    _rule_12_mpg_to_be_released(db, stats)
    return _finish(db, stats)


def regenerate_for_lot_monitoring(db: Session) -> Dict[str, int]:
    """After saving lot_monitoring → rules 6, 10, 13, 14."""
    stats: Dict[str, int] = {"created": 0, "deleted": 0}
    _rule_06_get_etd(db, stats)
    _rule_10_payment_application(db, stats)
    _rule_13_inspection_application(db, stats)
    _rule_14_get_shipping_documents(db, stats)
    return _finish(db, stats)


def regenerate_for_delivery_procedure(db: Session) -> Dict[str, int]:
    """After saving delivery_procedures → rules 7, 8, 9."""
    stats: Dict[str, int] = {"created": 0, "deleted": 0}
    _rule_07_get_customs_exemption(db, stats)
    _rule_08_prepare_asn(db, stats)
    _rule_09_create_delivery_note(db, stats)
    return _finish(db, stats)


# ─────────────────────────────────────────────
# Full regenerate (all 14 rules — use sparingly)
# ─────────────────────────────────────────────

def regenerate_all(db: Session) -> Dict[str, int]:
    """
    Re-evaluate every rule and upsert / prune reminders.
    Use for initial load or the /regenerate endpoint.
    Returns {"created": N, "deleted": N, "total_active": N}.
    """
    stats: Dict[str, int] = {"created": 0, "deleted": 0}

    _rule_01_tbg_to_be_issued(db, stats)
    _rule_02_pbg_to_be_issued(db, stats)
    _rule_03_tbg_to_be_released(db, stats)
    _rule_04_mpg_to_be_issued(db, stats)
    _rule_05_pbg_to_be_released(db, stats)
    _rule_06_get_etd(db, stats)
    _rule_07_get_customs_exemption(db, stats)
    _rule_08_prepare_asn(db, stats)
    _rule_09_create_delivery_note(db, stats)
    _rule_10_payment_application(db, stats)
    _rule_11_prepare_ld_statement(db, stats)
    _rule_12_mpg_to_be_released(db, stats)
    _rule_13_inspection_application(db, stats)
    _rule_14_get_shipping_documents(db, stats)

    return _finish(db, stats)