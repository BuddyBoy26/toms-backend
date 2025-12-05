from pydantic import BaseModel, Field
from typing import Optional, List, Annotated
from datetime import date
from decimal import Decimal

from app.models.tendering_companies import CurrencyEnum, PendingStatusEnum

Decimal12 = Annotated[Decimal, Field(..., max_digits=12, decimal_places=2)]
OptionalDecimal12 = Optional[Annotated[Decimal, Field(None, max_digits=12, decimal_places=2)]]

class TenderingCompaniesBase(BaseModel):
    company_id: int
    tender_id: int

    # Header / receipt section
    tender_receipt_no: Optional[str] = None
    debit_advice_no: Optional[str] = None
    debit_advice_date: Optional[date] = None

    # TBG details section
    tbg_credit_card_option: int = 0  # 0: TBG, 1: Credit Card
    tbg_no: Optional[str] = None
    tbg_issuing_bank: Optional[str] = None
    tender_deposit_receipt_no: Optional[str] = None
    tendering_currency: CurrencyEnum = CurrencyEnum.AED
    
    # Credit card fields (show if credit card is selected)
    credit_card_payment_ref: Optional[str] = None
    remarks: Optional[str] = None
    
    # Continue with TBG section
    tbg_value: OptionalDecimal12 = None
    tbg_date: Optional[date] = None
    tbg_expiry_date: Optional[date] = None
    tbg_submitted_date: Optional[date] = None
    tbg_release_date_dewa: Optional[date] = None
    tbg_release_date_bank: Optional[date] = None
    dewa_enbd_ref: Optional[str] = None
    
    # Tender extension dates (array)
    tender_extension_dates: Optional[List[date]] = None

    # Counter Guarantee Details section
    cg_bank: Optional[str] = None
    cg_no: Optional[str] = None
    cg_date: Optional[date] = None
    cg_expiry_date: Optional[date] = None

    # Delivery Weeks
    delivery_commencement_weeks: Optional[int] = None
    delivery_completion_weeks: Optional[int] = None

    # Status flags (6 radio buttons / checkboxes)
    tender_bought: bool = False
    participated: bool = False
    result_saved: bool = False
    evaluations_received: bool = False
    memo: bool = False
    po_copies: bool = False

class TenderingCompaniesCreate(TenderingCompaniesBase):
    pass

class TenderingCompaniesUpdate(BaseModel):
    company_id: Optional[int] = None
    tender_id: Optional[int] = None

    # Header / receipt section
    tender_receipt_no: Optional[str] = None
    debit_advice_no: Optional[str] = None
    debit_advice_date: Optional[date] = None

    # TBG details section
    tbg_credit_card_option: Optional[int] = None
    tbg_no: Optional[str] = None
    tbg_issuing_bank: Optional[str] = None
    tender_deposit_receipt_no: Optional[str] = None
    tendering_currency: Optional[CurrencyEnum] = None
    
    # Credit card fields
    credit_card_payment_ref: Optional[str] = None
    remarks: Optional[str] = None
    
    # Continue with TBG section
    tbg_value: OptionalDecimal12 = None
    tbg_date: Optional[date] = None
    tbg_expiry_date: Optional[date] = None
    tbg_submitted_date: Optional[date] = None
    tbg_release_date_dewa: Optional[date] = None
    tbg_release_date_bank: Optional[date] = None
    dewa_enbd_ref: Optional[str] = None
    
    # Tender extension dates
    tender_extension_dates: Optional[List[date]] = None

    # Counter Guarantee Details section
    cg_bank: Optional[str] = None
    cg_no: Optional[str] = None
    cg_date: Optional[date] = None
    cg_expiry_date: Optional[date] = None

    # Delivery Weeks
    delivery_commencement_weeks: Optional[int] = None
    delivery_completion_weeks: Optional[int] = None

    # Status flags
    tender_bought: Optional[bool] = None
    participated: Optional[bool] = None
    result_saved: Optional[bool] = None
    evaluations_received: Optional[bool] = None
    memo: Optional[bool] = None
    po_copies: Optional[bool] = None

class TenderingCompaniesRead(TenderingCompaniesBase):
    tendering_companies_id: int

    class Config:
        from_attributes = True