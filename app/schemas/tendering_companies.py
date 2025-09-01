from pydantic import BaseModel, Field
from typing import Optional, List, Annotated
from datetime import date
from decimal import Decimal

from app.models.tendering_companies import CurrencyEnum, PendingStatusEnum

Decimal12 = Annotated[Decimal, Field(..., max_digits=12, decimal_places=2)]
OptionalDecimal12 = Optional[Annotated[Decimal, Field(None, max_digits=12, decimal_places=2)]]
OptionalPercent = Optional[Annotated[Decimal, Field(None, max_digits=5, decimal_places=2)]]

class TenderingCompaniesBase(BaseModel):
    company_id: int
    tender_id: int

    # header
    tender_receipt_no: Optional[str] = None

    # TBG / deposit
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

    tender_extension_dates: Optional[List[date]] = None
    tendering_currency: CurrencyEnum = CurrencyEnum.AED
    discount_percent: OptionalPercent = None
    remarks: Optional[str] = None
    pending_status: PendingStatusEnum = PendingStatusEnum.TO_BE_RELEASED

    # boolean flags (as booleans at schema level)
    debit_advice_no: Optional[str] = None
    tender_bought: bool = False
    participated: bool = False
    result_saved: bool = False
    evaluations_received: bool = False
    memo: bool = False
    po_copies: bool = False

    # Counter Guarantee Details
    cg_bank: Optional[str] = None
    cg_no: Optional[str] = None
    cg_date: Optional[date] = None
    cg_expiry_date: Optional[date] = None

class TenderingCompaniesCreate(TenderingCompaniesBase):
    pass

class TenderingCompaniesUpdate(BaseModel):
    company_id: Optional[int] = None
    tender_id: Optional[int] = None

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

    tender_extension_dates: Optional[List[date]] = None
    tendering_currency: Optional[CurrencyEnum] = None
    discount_percent: OptionalPercent = None
    remarks: Optional[str] = None
    pending_status: Optional[PendingStatusEnum] = None

    debit_advice_no: Optional[str] = None
    tender_bought: Optional[bool] = None
    participated: Optional[bool] = None
    result_saved: Optional[bool] = None
    evaluations_received: Optional[bool] = None
    memo: Optional[bool] = None
    po_copies: Optional[bool] = None

    cg_bank: Optional[str] = None
    cg_no: Optional[str] = None
    cg_date: Optional[date] = None
    cg_expiry_date: Optional[date] = None

class TenderingCompaniesRead(TenderingCompaniesBase):
    tendering_companies_id: int

    class Config:
        from_attributes = True
