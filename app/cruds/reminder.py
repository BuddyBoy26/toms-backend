from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.reminder import Reminder, ReminderTypeEnum
from app.schemas.reminder import ReminderCreate, ReminderUpdate


# ─────────────────────────────────────────────
# Standard CRUD
# ─────────────────────────────────────────────

def get_reminders(db: Session, skip: int = 0, limit: int = 200) -> List[Reminder]:
    """Return all reminders ordered by activation_date ascending."""
    return (
        db.query(Reminder)
        .order_by(Reminder.activation_date.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_active_reminders(db: Session) -> List[Reminder]:
    """
    Return reminders where:
      • activation_date <= today
      • is_dismissed = False
    Ordered oldest-first.
    """
    today = date.today()
    return (
        db.query(Reminder)
        .filter(
            Reminder.activation_date <= today,
            Reminder.is_dismissed == False,
        )
        .order_by(Reminder.activation_date.asc())
        .all()
    )


def get_reminder(db: Session, reminder_id: int) -> Optional[Reminder]:
    return db.query(Reminder).filter(Reminder.reminder_id == reminder_id).first()


def create_reminder(db: Session, r: ReminderCreate) -> Reminder:
    db_obj = Reminder(**r.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_reminder(db: Session, reminder_id: int, r: ReminderUpdate) -> Optional[Reminder]:
    obj = get_reminder(db, reminder_id)
    if not obj:
        return None
    for field, value in r.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_reminder(db: Session, reminder_id: int) -> Optional[Reminder]:
    obj = get_reminder(db, reminder_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


# ─────────────────────────────────────────────
# Upsert helper (used by the reminder engine)
# ─────────────────────────────────────────────

def upsert_reminder(
    db: Session,
    reminder_type: ReminderTypeEnum,
    source_table: str,
    source_id: int,
    po_number: str,
    description: str,
    activation_date: date,
    order_id: Optional[int] = None,
) -> Reminder:
    """
    Insert a new reminder or update the existing one
    (matched on the unique key: reminder_type + source_table + source_id).
    If the reminder was previously dismissed and the underlying data changed,
    we leave is_dismissed as-is so users aren't nagged again.
    """
    existing = (
        db.query(Reminder)
        .filter(
            Reminder.reminder_type == reminder_type,
            Reminder.source_table == source_table,
            Reminder.source_id == source_id,
        )
        .first()
    )

    if existing:
        # Update mutable fields (description / po may have changed)
        existing.po_number = po_number
        existing.description = description
        existing.activation_date = activation_date
        existing.order_id = order_id
        db.commit()
        db.refresh(existing)
        return existing

    new_obj = Reminder(
        reminder_type=reminder_type,
        order_id=order_id,
        po_number=po_number,
        description=description,
        activation_date=activation_date,
        source_table=source_table,
        source_id=source_id,
    )
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj


def delete_reminders_by_source(
    db: Session,
    reminder_type: ReminderTypeEnum,
    source_table: str,
    source_id: int,
) -> int:
    """Delete a reminder when its condition no longer holds. Returns rows deleted."""
    count = (
        db.query(Reminder)
        .filter(
            Reminder.reminder_type == reminder_type,
            Reminder.source_table == source_table,
            Reminder.source_id == source_id,
        )
        .delete(synchronize_session="fetch")
    )
    db.commit()
    return count


def delete_all_auto_reminders(db: Session) -> int:
    """Wipe all engine-generated reminders so we can rebuild from scratch."""
    count = db.query(Reminder).delete(synchronize_session="fetch")
    db.commit()
    return count