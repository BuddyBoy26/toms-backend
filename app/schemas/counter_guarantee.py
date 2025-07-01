from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

from app.models.counter_guarantee import (
    GuaranteeTypeEnum,
    PendingStatusEnum,
)

class CounterGuaranteeBase(BaseModel):
    guarantee_type: GuaranteeTypeEnum
    guarantee_ref_number: str
    cg_date: date
    issuing_bank: Optional[str] = None
    expiry_date: date
    release_date_bank: Optional[date] = None
    remarks: Optional[str] = None
    pending_status: PendingStatusEnum = Field(default=PendingStatusEnum.NOT_ISSUED)

class CounterGuaranteeCreate(CounterGuaranteeBase):
    """All fields except cg_id."""

class CounterGuaranteeUpdate(BaseModel):
    guarantee_type: Optional[GuaranteeTypeEnum] = None
    guarantee_ref_number: Optional[str] = None
    cg_date: Optional[date] = None
    issuing_bank: Optional[str] = None
    expiry_date: Optional[date] = None
    release_date_bank: Optional[date] = None
    remarks: Optional[str] = None
    pending_status: Optional[PendingStatusEnum] = None

class CounterGuaranteeRead(CounterGuaranteeBase):
    cg_id: int

    class Config:
        from_attributes = True
