from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from datetime import date
from decimal import Decimal

# re‐use enums for client
from app.models.tendering_companies import CurrencyEnum, PendingStatusEnum

# Annotated types
Decimal12 = Annotated[Decimal, Field(..., max_digits=12, decimal_places=2)]
OptionalDecimal12 = Optional[Annotated[Decimal, Field(None, max_digits=12, decimal_places=2)]]

DateList = List[date]

class TenderingCompaniesBase(BaseModel):
    tender_id: int
    company_id: int
    tender_receipt_no: Optional[str] = None
    tbg_no: Optional[str] = None
    tbg_issuing_bank: Optional[str] = None
    tender_deposit_receipt_no: Optional[str] = None
    cheque_no: Optional[str] = None
    tt_ref: Optional[str] = None
    tt_date: Optional[date] = None
    document_date: Optional[date] = None
    tbg_value: OptionalDecimal12 = None
    tbg_expiry_date: Optional[date] = None
    tbg_submitted_date: Optional[date] = None
    tbg_release_date_dewa: Optional[date] = None
    tbg_release_date_bank: Optional[date] = None
    tender_extension_dates: Optional[DateList] = None
    tendering_currency: CurrencyEnum
    discount_percent: OptionalDecimal12 = None
    remarks: Optional[str] = None
    pending_status: PendingStatusEnum

class TenderingCompaniesCreate(TenderingCompaniesBase):
    """All required except auto‐PK."""

class TenderingCompaniesUpdate(BaseModel):
    tender_receipt_no: Optional[str] = None
    tbg_no: Optional[str] = None
    tbg_issuing_bank: Optional[str] = None
    tender_deposit_receipt_no: Optional[str] = None
    cheque_no: Optional[str] = None
    tt_ref: Optional[str] = None
    tt_date: Optional[date] = None
    document_date: Optional[date] = None
    tbg_value: OptionalDecimal12 = None
    tbg_expiry_date: Optional[date] = None
    tbg_submitted_date: Optional[date] = None
    tbg_release_date_dewa: Optional[date] = None
    tbg_release_date_bank: Optional[date] = None
    tender_extension_dates: Optional[DateList] = None
    tendering_currency: Optional[CurrencyEnum] = None
    discount_percent: OptionalDecimal12 = None
    remarks: Optional[str] = None
    pending_status: Optional[PendingStatusEnum] = None

class TenderingCompaniesRead(TenderingCompaniesBase):
    tendering_companies_id: int

    class Config:
        from_attributes = True
