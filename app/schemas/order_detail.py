from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from datetime import date
from decimal import Decimal
from app.models.order_detail import CurrencyEnum

# Constrained decimals
Decimal14 = Annotated[Decimal, Field(..., max_digits=14, decimal_places=2)]
OptionalDecimal14 = Optional[Annotated[Decimal, Field(None, max_digits=14, decimal_places=2)]]
Percent5  = Annotated[Decimal, Field(..., ge=0, le=100, decimal_places=2)]
OptionalPercent5 = Optional[Annotated[Decimal, Field(None, ge=0, le=100, decimal_places=2)]]

class OrderDetailBase(BaseModel):
    company_id: int
    tender_id: int
    po_number: str
    order_description: str
    order_date: date
    order_value: Decimal14
    currency: CurrencyEnum
    order_value_aed: Decimal14
    revised_value_lme: OptionalDecimal14 = None
    revised_value_lme_aed: OptionalDecimal14 = None
    order_confirmation_no: Optional[str] = None
    order_confirmation_date: Optional[date] = None
    po_confirmation_date_srm: Optional[date] = None
    drawing_submission_date: Optional[date] = None
    drawing_approval_date: Optional[date] = None
    last_contractual_delivery: Optional[date] = None
    actual_last_delivery: Optional[date] = None
    old_po_id: Optional[int] = None
    kka_commission_percent: Percent5 = Field(default=5.00)
    no_of_consignments: Optional[int] = None

class OrderDetailCreate(OrderDetailBase):
    """All fields in Base required except old_po_id may be null."""

class OrderDetailUpdate(BaseModel):
    company_id: Optional[int] = None
    tender_id: Optional[int] = None
    po_number: Optional[str] = None
    order_description: Optional[str] = None
    order_date: Optional[date] = None
    order_value: OptionalDecimal14 = None
    currency: Optional[CurrencyEnum] = None
    order_value_aed: OptionalDecimal14 = None
    revised_value_lme: OptionalDecimal14 = None
    revised_value_lme_aed: OptionalDecimal14 = None
    order_confirmation_no: Optional[str] = None
    order_confirmation_date: Optional[date] = None
    po_confirmation_date_srm: Optional[date] = None
    drawing_submission_date: Optional[date] = None
    drawing_approval_date: Optional[date] = None
    last_contractual_delivery: Optional[date] = None
    actual_last_delivery: Optional[date] = None
    old_po_id: Optional[int] = None
    kka_commission_percent: OptionalPercent5 = None
    no_of_consignments: Optional[int] = None

class OrderDetailRead(OrderDetailBase):
    order_id: int

    class Config:
        from_attributes = True
