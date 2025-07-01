from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class DiscrepancyBase(BaseModel):
    lot_id: str
    dewa_letter_ref: str
    letter_date: date
    pending_quantity: Optional[int] = None
    unit_sl_nos: Optional[str] = None
    discrepancies: str
    remarks: Optional[str] = None
    pending_status: bool = Field(default=True)
    resolution_date: Optional[date] = None
    delivery_note_no: Optional[str] = None
    actual_delivery_date: Optional[date] = None

class DiscrepancyCreate(DiscrepancyBase):
    """All fields except auto‐PK."""

class DiscrepancyUpdate(BaseModel):
    dewa_letter_ref: Optional[str] = None
    letter_date: Optional[date] = None
    pending_quantity: Optional[int] = None
    unit_sl_nos: Optional[str] = None
    discrepancies: Optional[str] = None
    remarks: Optional[str] = None
    pending_status: Optional[bool] = None
    resolution_date: Optional[date] = None
    delivery_note_no: Optional[str] = None
    actual_delivery_date: Optional[date] = None

class DiscrepancyRead(DiscrepancyBase):
    discrepancy_id: int

    class Config:
        from_attributes = True
