# schemas/discrepancy.py
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# Sub-schema to validate the individual items in the JSON array
class DiscrepancyDetail(BaseModel):
    qty: int
    nature_of_discrepancy: str
    remarks: Optional[str] = None
    pending_status: bool = Field(default=True)
    delivery_note_no: Optional[str] = None
    delivery_date: Optional[date] = None

class DiscrepancyBase(BaseModel):
    lot_id: int
    dewa_letter_ref: Optional[str] = None
    letter_date: Optional[date] = None
    total_discrepant_units: Optional[int] = None
    
    # The array of rows
    details: List[DiscrepancyDetail]

class DiscrepancyCreate(DiscrepancyBase):
    """All fields except auto-PK."""

class DiscrepancyUpdate(BaseModel):
    dewa_letter_ref: Optional[str] = None
    letter_date: Optional[date] = None
    total_discrepant_units: Optional[int] = None
    details: Optional[List[DiscrepancyDetail]] = None

class DiscrepancyRead(DiscrepancyBase):
    discrepancy_id: int

    class Config:
        from_attributes = True