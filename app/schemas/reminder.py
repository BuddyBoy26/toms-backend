from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.reminder import ReminderTypeEnum


# -------------------------
# Base
# -------------------------

class ReminderBase(BaseModel):
    reminder_type: ReminderTypeEnum
    order_id: Optional[int] = None
    po_number: str
    description: str
    activation_date: date
    is_dismissed: bool = False
    source_table: str
    source_id: int


# -------------------------
# Create  (used internally by the engine — not exposed via POST)
# -------------------------

class ReminderCreate(ReminderBase):
    pass


# -------------------------
# Update  (only dismissal toggle is user-facing)
# -------------------------

class ReminderUpdate(BaseModel):
    is_dismissed: Optional[bool] = None


# -------------------------
# Read
# -------------------------

class ReminderRead(ReminderBase):
    reminder_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# -------------------------
# Summary returned by the regenerate endpoint
# -------------------------

class ReminderRegenerateSummary(BaseModel):
    created: int
    deleted: int
    total_active: int