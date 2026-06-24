from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import app.cruds.reminder as cruds
import app.schemas.reminder as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User
from app.utils.reminder_engine import (
    regenerate_all,
    regenerate_for_tendering_companies,
    regenerate_for_order_details,
    regenerate_for_performance_guarantee,
    regenerate_for_material_performance_guarantee,
    regenerate_for_lot_monitoring,
    regenerate_for_delivery_procedure,
)

router = APIRouter(tags=["reminders"])


# ─────────────────────────────────────────────
# Regenerate — full (all 14 rules)
# ─────────────────────────────────────────────

@router.post(
    "/regenerate",
    response_model=schemas.ReminderRegenerateSummary,
    summary="Re-evaluate ALL 14 rules (use on first load or manually)",
)
def regen_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = regenerate_all(db)
    return schemas.ReminderRegenerateSummary(**result)


# ─────────────────────────────────────────────
# Regenerate — targeted (only rules for one table)
# ─────────────────────────────────────────────

@router.post(
    "/regenerate/tendering_companies",
    response_model=schemas.ReminderRegenerateSummary,
    summary="Rule 1 only — after saving tendering company details",
)
def regen_tendering_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return schemas.ReminderRegenerateSummary(**regenerate_for_tendering_companies(db))


@router.post(
    "/regenerate/order_details",
    response_model=schemas.ReminderRegenerateSummary,
    summary="Rules 2, 4, 11 — after saving an order",
)
def regen_order_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return schemas.ReminderRegenerateSummary(**regenerate_for_order_details(db))


@router.post(
    "/regenerate/performance_guarantee",
    response_model=schemas.ReminderRegenerateSummary,
    summary="Rule 3 — after saving a PBG",
)
def regen_performance_guarantee(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return schemas.ReminderRegenerateSummary(**regenerate_for_performance_guarantee(db))


@router.post(
    "/regenerate/material_performance_guarantee",
    response_model=schemas.ReminderRegenerateSummary,
    summary="Rules 5, 12 — after saving an MPG",
)
def regen_mpg(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return schemas.ReminderRegenerateSummary(**regenerate_for_material_performance_guarantee(db))


@router.post(
    "/regenerate/lot_monitoring",
    response_model=schemas.ReminderRegenerateSummary,
    summary="Rules 6, 10, 13, 14 — after saving lot monitoring",
)
def regen_lot_monitoring(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return schemas.ReminderRegenerateSummary(**regenerate_for_lot_monitoring(db))


@router.post(
    "/regenerate/delivery_procedure",
    response_model=schemas.ReminderRegenerateSummary,
    summary="Rules 7, 8, 9 — after saving a delivery procedure",
)
def regen_delivery_procedure(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return schemas.ReminderRegenerateSummary(**regenerate_for_delivery_procedure(db))


# ─────────────────────────────────────────────
# List endpoints
# ─────────────────────────────────────────────

@router.get(
    "/",
    response_model=List[schemas.ReminderRead],
    summary="List all reminders (including future & dismissed)",
)
def list_reminders(
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_reminders(db, skip, limit)


@router.get(
    "/active",
    response_model=List[schemas.ReminderRead],
    summary="List only active reminders (activation_date <= today, not dismissed)",
)
def list_active_reminders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_active_reminders(db)


# ─────────────────────────────────────────────
# Single reminder
# ─────────────────────────────────────────────

@router.get(
    "/{reminder_id}",
    response_model=schemas.ReminderRead,
)
def read_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_reminder(db, reminder_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return obj


# ─────────────────────────────────────────────
# Dismiss / un-dismiss
# ─────────────────────────────────────────────

@router.patch(
    "/{reminder_id}",
    response_model=schemas.ReminderRead,
    summary="Update a reminder (typically to dismiss or un-dismiss)",
)
def update_reminder(
    reminder_id: int,
    r: schemas.ReminderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_reminder(db, reminder_id, r)
    if not obj:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return obj


@router.patch(
    "/{reminder_id}/dismiss",
    response_model=schemas.ReminderRead,
    summary="Shortcut: dismiss a single reminder",
)
def dismiss_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_reminder(
        db, reminder_id, schemas.ReminderUpdate(is_dismissed=True)
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return obj


# ─────────────────────────────────────────────
# No hard-delete endpoint exposed.
# ─────────────────────────────────────────────
# Dismissed reminders survive regeneration (is_dismissed stays True).
# Hard-deleting would let regeneration recreate the reminder.
# The engine's own _cleanup() handles deletion when conditions
# no longer hold (e.g. TBG was finally issued → reminder removed).