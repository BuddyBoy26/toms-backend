from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List, Annotated
from datetime import date
from decimal import Decimal

from app.models.performance_guarantee import PBGStatusEnum

# Constrained decimal
Decimal12 = Annotated[Decimal, Field(..., max_digits=12, decimal_places=2)]
DateList  = List[date]

class PerformanceGuaranteeBase(BaseModel):
    order_id: int
    pg_no: str
    pg_issuing_bank: Optional[str] = None
    pg_deposit_receipt_no: Optional[str] = None
    cheque_no: Optional[str] = None
    tt_date: Optional[date] = None
    document_date: Optional[date] = None
    pg_value: Decimal12
    pg_expiry_date: date
    pg_submitted_date: Optional[date] = None
    pg_return_date: Optional[date] = None
    pg_release_date_dewa: Optional[date] = None
    pg_release_date_bank: Optional[date] = None
    pg_extension_dates: Optional[DateList] = None
    remarks: Optional[str] = None
    pending_status: PBGStatusEnum = Field(default=PBGStatusEnum.NOT_ISSUED)

class PerformanceGuaranteeCreate(PerformanceGuaranteeBase):
    """All fields except the auto‐PK."""

class PerformanceGuaranteeUpdate(BaseModel):
    pg_no: Optional[str] = None
    pg_issuing_bank: Optional[str] = None
    pg_deposit_receipt_no: Optional[str] = None
    cheque_no: Optional[str] = None
    tt_date: Optional[date] = None
    document_date: Optional[date] = None
    pg_value: Optional[Decimal12] = None
    pg_expiry_date: Optional[date] = None
    pg_submitted_date: Optional[date] = None
    pg_return_date: Optional[date] = None
    pg_release_date_dewa: Optional[date] = None
    pg_release_date_bank: Optional[date] = None
    pg_extension_dates: Optional[DateList] = None
    remarks: Optional[str] = None
    pending_status: Optional[PBGStatusEnum] = None

class PerformanceGuaranteeRead(PerformanceGuaranteeBase):
    pg_id: int

    class Config:
        from_attributes = True
