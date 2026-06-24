"""
services/reminder_triggers.py

UPDATED:
  - handle_mpg_update: watches mpg_release_date → resolves MPG Release reminder
  - handle_po_update:  watches advised_date_of_inspection → resolves Inspection
                       Application reminder; etd_date → also resolves ETD reminder
                       (in addition to creating Shipping Documents reminder)
  - handle_pbg_update, handle_tbg_update, handle_tender_update, handle_lot_update:
    unchanged from last version

These resolves complement services/date_checks.py: date_checks creates the
time-based reminders on GET /reminders; the triggers here resolve them the
moment the user saves the relevant field via the API.
"""

from typing import Any, Mapping, Optional

from sqlalchemy.orm import Session

from app.cruds import reminder as reminder_crud


# ---- Object type constants -------------------------------------------------
OBJ_MPG = "MPG"
OBJ_PO = "PO"
OBJ_TBG = "TBG"
OBJ_PBG = "PBG"
OBJ_TENDER = "Tender"
OBJ_LOT = "Lot"
OBJ_DISCREPANCY = "Discrepancy"
OBJ_DELIVERY_PROCEDURE = "DeliveryProcedure"


# ---- Helpers ---------------------------------------------------------------
def _is_empty(v: Any) -> bool:
    return v is None or v == ""


def _became_set(before: Mapping[str, Any], after: Mapping[str, Any], field: str) -> bool:
    return _is_empty(before.get(field)) and not _is_empty(after.get(field))


def _value_changed_to(
    before: Mapping[str, Any], after: Mapping[str, Any], field: str, target: Any
) -> bool:
    return before.get(field) != target and after.get(field) == target


# ============================================================================
# TENDER
# ============================================================================
def handle_tender_update(
    db: Session,
    *,
    tender_no: str,
    before: Mapping[str, Any],
    after: Mapping[str, Any],
) -> None:
    object_id = str(tender_no)

    # TBG Reminder (cross-object: lives on Tender, resolved by TBG update)
    desc = f"TBG date for Tender No. ({tender_no}) has to be entered"
    if _became_set(before, after, "tender_receipt_date"):
        reminder_crud.upsert_active_reminder(
            db, object=OBJ_TENDER, object_id=object_id, description=desc
        )


# ============================================================================
# TBG
# ============================================================================
def handle_tbg_update(
    db: Session,
    *,
    tbg_no: str,
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    parent_tender_no: Optional[str] = None,
    related_pbg_no: Optional[str] = None,
) -> None:
    # Resolve TBG Reminder on parent Tender
    if _became_set(before, after, "tbg_date") and parent_tender_no is not None:
        desc = f"TBG date for Tender No. ({parent_tender_no}) has to be entered"
        reminder_crud.resolve_reminders(
            db, object=OBJ_TENDER, object_id=str(parent_tender_no), description_match=desc
        )

    # Resolve TBG Release on related PBG
    if _became_set(before, after, "tbg_release_date") and related_pbg_no is not None:
        desc = f"TBG Release Date (DEWA) for PBG No. ({related_pbg_no}) has to be entered"
        reminder_crud.resolve_reminders(
            db, object=OBJ_PBG, object_id=str(related_pbg_no), description_match=desc
        )


# ============================================================================
# PBG
# ============================================================================
def handle_pbg_update(
    db: Session,
    *,
    pbg_no: str,
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    parent_po_no: Optional[str] = None,
    related_mpg_no: Optional[str] = None,
) -> None:
    object_id = str(pbg_no)

    # CREATE TBG Release reminder on this PBG
    desc_tbg_release = f"TBG Release Date (DEWA) for PBG No. ({pbg_no}) has to be entered"
    if _became_set(before, after, "pbg_date"):
        reminder_crud.upsert_active_reminder(
            db, object=OBJ_PBG, object_id=object_id, description=desc_tbg_release
        )

    # RESOLVE PBG Reminder on parent PO
    if _became_set(before, after, "pbg_date") and parent_po_no is not None:
        desc = f"PBG date for PO No. ({parent_po_no}) has to be entered"
        reminder_crud.resolve_reminders(
            db, object=OBJ_PO, object_id=str(parent_po_no), description_match=desc
        )

    # RESOLVE PBG Release on related MPG
    if _became_set(before, after, "pbg_release_date") and related_mpg_no is not None:
        desc = f"PBG Release Date (DEWA) for MPG No. ({related_mpg_no}) has to be entered"
        reminder_crud.resolve_reminders(
            db, object=OBJ_MPG, object_id=str(related_mpg_no), description_match=desc
        )


# ============================================================================
# MPG
# ============================================================================
def handle_mpg_update(
    db: Session,
    *,
    mpg_no: str,
    before: Mapping[str, Any],
    after: Mapping[str, Any],
) -> None:
    object_id = str(mpg_no)

    # --- MPG Reminder (same-object) ----------------------------------------
    desc_mpg = f"MPG date for guarantee No. ({mpg_no}) has to be entered"
    if _became_set(before, after, "actual_last_delivery_date") and _is_empty(after.get("mpg_date")):
        reminder_crud.upsert_active_reminder(
            db, object=OBJ_MPG, object_id=object_id, description=desc_mpg
        )
    if _became_set(before, after, "mpg_date"):
        reminder_crud.resolve_reminders(
            db, object=OBJ_MPG, object_id=object_id, description_match=desc_mpg
        )

    # --- PBG Release (cross-object CREATE: lives on MPG) -------------------
    desc_pbg_release = f"PBG Release Date (DEWA) for MPG No. ({mpg_no}) has to be entered"
    if _became_set(before, after, "mpg_date"):
        reminder_crud.upsert_active_reminder(
            db, object=OBJ_MPG, object_id=object_id, description=desc_pbg_release
        )

    # --- MPG Release (RESOLVE when mpg_release_date is entered) ------------
    # Created by date_checks.py when expiry date is reached; resolved here
    # the moment the user saves mpg_release_date via the API.
    desc_mpg_release = f"MPG Release Date (DEWA) for guarantee No. ({mpg_no}) has to be entered"
    if _became_set(before, after, "mpg_release_date"):
        reminder_crud.resolve_reminders(
            db, object=OBJ_MPG, object_id=object_id, description_match=desc_mpg_release
        )


# ============================================================================
# PO
# ============================================================================
def handle_po_update(
    db: Session,
    *,
    po_no: str,
    before: Mapping[str, Any],
    after: Mapping[str, Any],
) -> None:
    object_id = str(po_no)

    # --- PBG Reminder (cross-object CREATE on PO creation) -----------------
    desc = f"PBG date for PO No. ({po_no}) has to be entered"
    if _became_set(before, after, "po_no"):
        reminder_crud.upsert_active_reminder(
            db, object=OBJ_PO, object_id=object_id, description=desc
        )

    # --- ETD Reminder (RESOLVE when etd_date is entered) ------------------
    # Created by date_checks.py 1 week after dispatch_clearance_date;
    # resolved here the moment the user saves etd_date via the API.
    desc_etd = f"ETD date for PO No. ({po_no}) has to be received from Principals"
    if _became_set(before, after, "etd_date"):
        reminder_crud.resolve_reminders(
            db, object=OBJ_PO, object_id=object_id, description_match=desc_etd
        )

    # --- Shipping Documents -----------------------------------------------
    desc = f"B/L for PO No. ({po_no}) has to be received from Principals"
    if _became_set(before, after, "etd_date") and after.get("document_status") != "Received":
        reminder_crud.upsert_active_reminder(
            db, object=OBJ_PO, object_id=object_id, description=desc
        )
    if _value_changed_to(before, after, "document_status", "Received"):
        reminder_crud.resolve_reminders(
            db, object=OBJ_PO, object_id=object_id, description_match=desc
        )

    # --- Customs Exemption / BL Stamping ----------------------------------
    desc = (
        f"Documents to Agent Date for PO No. ({po_no}) has to be entered "
        f"(Customs Exemption / BL Stamping)"
    )
    if (
        _value_changed_to(before, after, "document_status", "Received")
        and _is_empty(after.get("documents_to_agent_date"))
    ):
        reminder_crud.upsert_active_reminder(
            db, object=OBJ_PO, object_id=object_id, description=desc
        )
    if _became_set(before, after, "documents_to_agent_date"):
        reminder_crud.resolve_reminders(
            db, object=OBJ_PO, object_id=object_id, description_match=desc
        )

    # --- ASN reminder -----------------------------------------------------
    desc = f"Advanced Shipping Notification (ASN) for PO No. ({po_no}) has to be sent"
    if (
        _became_set(before, after, "documents_to_agent_date")
        and _is_empty(after.get("delivery_intimation_to_dewa_date"))
    ):
        reminder_crud.upsert_active_reminder(
            db, object=OBJ_PO, object_id=object_id, description=desc
        )
    if _became_set(before, after, "delivery_intimation_to_dewa_date"):
        reminder_crud.resolve_reminders(
            db, object=OBJ_PO, object_id=object_id, description_match=desc
        )

    # --- Create Delivery Note ---------------------------------------------
    desc = f"Delivery Note for PO No. ({po_no}) has to be created"
    if (
        _became_set(before, after, "delivery_intimation_to_dewa_date")
        and _is_empty(after.get("delivery_note_date"))
    ):
        reminder_crud.upsert_active_reminder(
            db, object=OBJ_PO, object_id=object_id, description=desc
        )
    if _became_set(before, after, "delivery_note_date"):
        reminder_crud.resolve_reminders(
            db, object=OBJ_PO, object_id=object_id, description_match=desc
        )

    # --- Create Gate Pass -------------------------------------------------
    desc = f"Gate Pass for PO No. ({po_no}) has to be created"
    if (
        _became_set(before, after, "delivery_note_date")
        and _is_empty(after.get("gate_pass_date"))
    ):
        reminder_crud.upsert_active_reminder(
            db, object=OBJ_PO, object_id=object_id, description=desc
        )
    if _became_set(before, after, "gate_pass_date"):
        reminder_crud.resolve_reminders(
            db, object=OBJ_PO, object_id=object_id, description_match=desc
        )

    # --- Apply for Payment ------------------------------------------------
    desc = f"Application for Payment for PO No. ({po_no}) has to be submitted"
    if (
        _became_set(before, after, "delivery_date")
        and _is_empty(after.get("application_for_payment_date"))
    ):
        reminder_crud.upsert_active_reminder(
            db, object=OBJ_PO, object_id=object_id, description=desc
        )
    if _became_set(before, after, "application_for_payment_date"):
        reminder_crud.resolve_reminders(
            db, object=OBJ_PO, object_id=object_id, description_match=desc
        )

    # --- Inspection Application (RESOLVE when advised_date_of_inspection entered)
    # Created by date_checks.py 90 days before contractual delivery;
    # resolved here the moment the user saves the field via the API.
    desc_insp = f"Inspection Application for PO No. ({po_no}) has to be submitted"
    if _became_set(before, after, "advised_date_of_inspection"):
        reminder_crud.resolve_reminders(
            db, object=OBJ_PO, object_id=object_id, description_match=desc_insp
        )


# ============================================================================
# LOT
# ============================================================================
def handle_lot_update(
    db: Session,
    *,
    lot_no: str,
    before: Mapping[str, Any],
    after: Mapping[str, Any],
) -> None:
    object_id = str(lot_no)

    # Send LD to DEWA — no auto-resolve field confirmed yet, resolved manually
    desc = f"LD has to be sent to DEWA for Lot No. ({lot_no})"
    if _became_set(before, after, "actual_last_delivery_date"):
        reminder_crud.upsert_active_reminder(
            db, object=OBJ_LOT, object_id=object_id, description=desc
        )
    # TODO: add resolve_reminders call when the resolve field is confirmed