# schemas/counter_guarantee.py
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum

class GuaranteeTypeEnum(str, Enum):
    TBG = "TBG"
    PBG = "PBG"
    MPG = "MPG"

class PendingStatusEnum(str, Enum):
    NOT_ISSUED         = "NOT Issued"
    ISSUED_EXTENDED    = "Issued / Extended"
    EXTENSION_REQUIRED = "Extension Required"
    NOT_RELEASED       = "NOT Released"
    RELEASED           = "Released"

class CounterGuaranteeBase(BaseModel):
    guarantee_type: GuaranteeTypeEnum
    guarantee_ref_number: str
    cg_date: date
    issuing_bank: Optional[str] = None
    expiry_date: date
    remarks: Optional[str] = None
    pending_status: PendingStatusEnum = Field(default=PendingStatusEnum.NOT_ISSUED)

class CounterGuaranteeCreate(CounterGuaranteeBase):
    pass

class CounterGuaranteeUpdate(BaseModel):
    # All fields optional for partial updates
    guarantee_type: Optional[GuaranteeTypeEnum] = None
    guarantee_ref_number: Optional[str] = None
    cg_date: Optional[date] = None
    issuing_bank: Optional[str] = None
    expiry_date: Optional[date] = None
    remarks: Optional[str] = None
    pending_status: Optional[PendingStatusEnum] = None

class CounterGuaranteeRead(CounterGuaranteeBase):
    cg_id: int

    class Config:
        from_attributes = True