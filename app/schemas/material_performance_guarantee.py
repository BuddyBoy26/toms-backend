from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List, Annotated
from datetime import date
from decimal import Decimal

from app.models.material_performance_guarantee import MPGStatusEnum

# Constrained decimal
Decimal12 = Annotated[Decimal, Field(..., max_digits=12, decimal_places=2)]
DateList  = List[date]

class MaterialPerformanceGuaranteeBase(BaseModel):
    order_id: int
    mpg_no: str
    mpg_issuing_bank: Optional[str] = None
    mpg_deposit_receipt_no: Optional[str] = None
    cheque_no: Optional[str] = None
    tt_date: Optional[date] = None
    document_date: Optional[date] = None
    mpg_value: Decimal12
    mpg_expiry_date: date
    mpg_submitted_date: Optional[date] = None
    mpg_return_date: Optional[date] = None
    mpg_release_date_dewa: Optional[date] = None
    mpg_release_date_bank: Optional[date] = None
    mpg_extension_dates: Optional[DateList] = None
    remarks: Optional[str] = None
    pending_status: MPGStatusEnum = Field(default=MPGStatusEnum.NOT_ISSUED)

class MaterialPerformanceGuaranteeCreate(MaterialPerformanceGuaranteeBase):
    """All fields except auto‐PK."""

class MaterialPerformanceGuaranteeUpdate(BaseModel):
    mpg_no: Optional[str] = None
    mpg_issuing_bank: Optional[str] = None
    mpg_deposit_receipt_no: Optional[str] = None
    cheque_no: Optional[str] = None
    tt_date: Optional[date] = None
    document_date: Optional[date] = None
    mpg_value: Optional[Decimal12] = None
    mpg_expiry_date: Optional[date] = None
    mpg_submitted_date: Optional[date] = None
    mpg_return_date: Optional[date] = None
    mpg_release_date_dewa: Optional[date] = None
    mpg_release_date_bank: Optional[date] = None
    mpg_extension_dates: Optional[DateList] = None
    remarks: Optional[str] = None
    pending_status: Optional[MPGStatusEnum] = None

class MaterialPerformanceGuaranteeRead(MaterialPerformanceGuaranteeBase):
    mpg_id: int

    class Config:
        from_attributes = True
