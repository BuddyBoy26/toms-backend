# schemas/material_performance_guarantee.py
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum

class MPGStatusEnum(str, Enum):
    NOT_ISSUED         = "NOT Issued"
    ISSUED_EXTENDED    = "Issued / Extended"
    EXTENSION_REQUIRED = "Extension Required"
    NOT_RELEASED       = "NOT Released"
    RELEASED           = "Released"

class MaterialPerformanceGuaranteeBase(BaseModel):
    order_id: int
    mpg_no: str
    participated: int = Field(default=0)
    mpg_bank_or_deposit: int = Field(default=0) # 0: Bank, 1: Deposit
    mpg_issuing_bank: Optional[str] = None
    mpg_deposit_receipt_no: Optional[str] = None
    mpg_value: float
    mpg_expiry_date: date
    mpg_submitted_date: Optional[date] = None
    mpg_release_date_dewa: Optional[date] = None
    mpg_release_date_bank: Optional[date] = None
    mpg_extension_dates: Optional[List[date]] = None
    remarks: Optional[str] = None
    pending_status: MPGStatusEnum = Field(default=MPGStatusEnum.NOT_ISSUED)

class MaterialPerformanceGuaranteeCreate(MaterialPerformanceGuaranteeBase):
    pass

class MaterialPerformanceGuaranteeUpdate(BaseModel):
    # All fields optional for partial updates
    order_id: Optional[int] = None
    mpg_no: Optional[str] = None
    participated: Optional[int] = None
    mpg_bank_or_deposit: Optional[int] = None
    mpg_issuing_bank: Optional[str] = None
    mpg_deposit_receipt_no: Optional[str] = None
    mpg_value: Optional[float] = None
    mpg_expiry_date: Optional[date] = None
    mpg_submitted_date: Optional[date] = None
    mpg_release_date_dewa: Optional[date] = None
    mpg_release_date_bank: Optional[date] = None
    mpg_extension_dates: Optional[List[date]] = None
    remarks: Optional[str] = None
    pending_status: Optional[MPGStatusEnum] = None

class MaterialPerformanceGuaranteeRead(MaterialPerformanceGuaranteeBase):
    mpg_id: int

    class Config:
        from_attributes = True