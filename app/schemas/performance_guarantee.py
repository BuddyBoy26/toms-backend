# schemas/performance_guarantee.py
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum

class PBGStatusEnum(str, Enum):
    NOT_ISSUED         = "NOT Issued"
    ISSUED_EXTENDED    = "Issued / Extended"
    EXTENSION_REQUIRED = "Extension Required"
    NOT_RELEASED       = "NOT Released"
    RELEASED           = "Released"

class PerformanceGuaranteeBase(BaseModel):
    order_id: int
    pg_no: str
    pg_bank_or_deposit: int = Field(default=0) # 0: Bank, 1: Deposit
    pg_issuing_bank: Optional[str] = None
    pg_deposit_receipt_no: Optional[str] = None
    pg_value: float
    pg_expiry_date: date
    pg_submitted_date: Optional[date] = None
    pg_release_date_dewa: Optional[date] = None
    pg_release_date_bank: Optional[date] = None
    pg_extension_dates: Optional[List[date]] = None
    remarks: Optional[str] = None
    pending_status: PBGStatusEnum = Field(default=PBGStatusEnum.NOT_ISSUED)

class PerformanceGuaranteeCreate(PerformanceGuaranteeBase):
    pass

class PerformanceGuaranteeUpdate(BaseModel):
    # All fields optional for partial updates
    order_id: Optional[int] = None
    pg_no: Optional[str] = None
    pg_bank_or_deposit: Optional[int] = None
    pg_issuing_bank: Optional[str] = None
    pg_deposit_receipt_no: Optional[str] = None
    pg_value: Optional[float] = None
    pg_expiry_date: Optional[date] = None
    pg_submitted_date: Optional[date] = None
    pg_release_date_dewa: Optional[date] = None
    pg_release_date_bank: Optional[date] = None
    pg_extension_dates: Optional[List[date]] = None
    remarks: Optional[str] = None
    pending_status: Optional[PBGStatusEnum] = None

class PerformanceGuaranteeRead(PerformanceGuaranteeBase):
    pg_id: int

    class Config:
        from_attributes = True