"""
services/date_checks.py

Handles the 3 time-based reminders by checking date conditions on every
GET /reminders call. No scheduler needed.

The 3 reminders handled here:
  1. MPG Release         – on reaching expiry date – until mpg_release_date entered
  2. Inspection Application – from 90 days before contractual delivery date –
                             until advised_date_of_inspection entered
  3. ETD Reminder        – from 1 week after dispatch_clearance_date –
                             until etd_date received from Principals

IMPORTANT: Adjust the model imports and field names below to match your
actual MPG and PO models. The field name assumptions are listed per function.
"""

from datetime import date, timedelta

from sqlalchemy.orm import Session

import app.cruds.reminder as reminder_crud

# Adjust these imports to your actual model locations
from app.models.material_performance_guarantee import MaterialPerformanceGuarantee  # <-- adjust import
from app.models.order_detail import OrderDetail    # <-- adjust import

OBJ_MPG = "MPG"
OBJ_PO = "PO"


def run_date_checks(db: Session) -> None:
    """
    Entry point. Called by GET /reminders before returning results.
    All three checks are idempotent — safe to run on every request.
    """
    today = date.today()
    _check_mpg_release(db, today)
    _check_inspection_application(db, today)
    _check_etd_reminder(db, today)


# ============================================================================
# 1. MPG Release
# ============================================================================
# Assumed MPG fields:
#   mpg_no            – user-facing identifier (string)
#   mpg_expiry_date   – the date on which the MPG expires (Date)
#   mpg_release_date  – set when DEWA releases the MPG (Date, nullable)
# ============================================================================
def _check_mpg_release(db: Session, today: date) -> None:
    desc_template = "MPG Release Date (DEWA) for guarantee No. ({mpg_no}) has to be entered"

    # CREATE: expiry date reached, release date not yet entered
    due = (
        db.query(MPG)
        .filter(
            MPG.mpg_expiry_date.isnot(None),
            MPG.mpg_expiry_date <= today,
            MPG.mpg_release_date.is_(None),
        )
        .all()
    )
    for mpg in due:
        reminder_crud.upsert_active_reminder(
            db,
            object=OBJ_MPG,
            object_id=str(mpg.mpg_no),
            description=desc_template.format(mpg_no=mpg.mpg_no),
        )

    # RESOLVE: release date now entered (safety net in case the update
    # endpoint didn't fire the resolve, e.g. data imported directly to DB)
    released = (
        db.query(MPG)
        .filter(MPG.mpg_release_date.isnot(None))
        .all()
    )
    for mpg in released:
        reminder_crud.resolve_reminders(
            db,
            object=OBJ_MPG,
            object_id=str(mpg.mpg_no),
            description_match=desc_template.format(mpg_no=mpg.mpg_no),
        )


# ============================================================================
# 2. Inspection Application
# ============================================================================
# Assumed PO fields:
#   po_no                      – user-facing identifier (string)
#   contractual_delivery_date  – the agreed delivery deadline (Date, nullable)
#   advised_date_of_inspection – set when inspection application is sent (Date, nullable)
# ============================================================================
def _check_inspection_application(db: Session, today: date) -> None:
    desc_template = (
        "Inspection Application for PO No. ({po_no}) has to be submitted"
    )
    threshold = today + timedelta(days=90)

    # CREATE: within 90 days of contractual delivery, inspection not yet applied
    due = (
        db.query(PO)
        .filter(
            PO.contractual_delivery_date.isnot(None),
            PO.contractual_delivery_date <= threshold,
            PO.advised_date_of_inspection.is_(None),
        )
        .all()
    )
    for po in due:
        reminder_crud.upsert_active_reminder(
            db,
            object=OBJ_PO,
            object_id=str(po.po_no),
            description=desc_template.format(po_no=po.po_no),
        )

    # RESOLVE: inspection application now sent (safety net)
    inspected = (
        db.query(PO)
        .filter(PO.advised_date_of_inspection.isnot(None))
        .all()
    )
    for po in inspected:
        reminder_crud.resolve_reminders(
            db,
            object=OBJ_PO,
            object_id=str(po.po_no),
            description_match=desc_template.format(po_no=po.po_no),
        )


# ============================================================================
# 3. ETD Reminder
# ============================================================================
# Assumed PO fields:
#   po_no                    – user-facing identifier (string)
#   dispatch_clearance_date  – date DEWA dispatch clearance was received (Date, nullable)
#   etd_date                 – estimated time of dispatch from Principals (Date, nullable)
# ============================================================================
def _check_etd_reminder(db: Session, today: date) -> None:
    desc_template = (
        "ETD date for PO No. ({po_no}) has to be received from Principals"
    )
    one_week_ago = today - timedelta(days=7)

    # CREATE: 1 week has passed since dispatch clearance, ETD not yet received
    due = (
        db.query(PO)
        .filter(
            PO.dispatch_clearance_date.isnot(None),
            PO.dispatch_clearance_date <= one_week_ago,
            PO.etd_date.is_(None),
        )
        .all()
    )
    for po in due:
        reminder_crud.upsert_active_reminder(
            db,
            object=OBJ_PO,
            object_id=str(po.po_no),
            description=desc_template.format(po_no=po.po_no),
        )

    # RESOLVE: ETD date now received (safety net)
    with_etd = (
        db.query(PO)
        .filter(PO.etd_date.isnot(None))
        .all()
    )
    for po in with_etd:
        reminder_crud.resolve_reminders(
            db,
            object=OBJ_PO,
            object_id=str(po.po_no),
            description_match=desc_template.format(po_no=po.po_no),
        )