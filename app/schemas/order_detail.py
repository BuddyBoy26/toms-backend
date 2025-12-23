from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from datetime import date
from decimal import Decimal
from app.models.order_detail import CurrencyEnum

# -------------------------
# Decimal constraints
# -------------------------

Decimal14_4 = Annotated[
    Decimal,
    Field(..., max_digits=14, decimal_places=4)
]

OptionalDecimal14_4 = Optional[
    Annotated[Decimal, Field(None, max_digits=14, decimal_places=4)]
]

Percent5_2 = Annotated[
    Decimal,
    Field(..., ge=0, le=100, max_digits=5, decimal_places=2)
]

OptionalPercent5_2 = Optional[
    Annotated[Decimal, Field(None, ge=0, le=100, max_digits=5, decimal_places=2)]
]

# -------------------------
# Base schema
# -------------------------

class OrderDetailBase(BaseModel):
    company_id: int
    tender_id: int
    po_number: str
    order_description: str
    order_date: date

    # ⚠ MATCH MODEL TYPO
    po_commencemnt_date: Optional[date] = None

    order_value: Decimal14_4
    currency: CurrencyEnum
    order_value_aed: Decimal14_4

    revised_value_lme: OptionalDecimal14_4 = None
    revised_value_lme_aed: OptionalDecimal14_4 = None

    kka_commission_percent: Percent5_2 = Field(default=Decimal("5.00"))

    old_po_id: Optional[int] = None
    no_of_consignments: Optional[int] = None

    order_confirmation_no: Optional[str] = None
    order_confirmation_letter_ref: Optional[str] = None
    order_confirmation_date: Optional[date] = None
    po_confirmation_date_srm: Optional[date] = None

    last_contractual_delivery: Optional[date] = None
    actual_last_delivery: Optional[date] = None

    drawing_submission_date: Optional[date] = None
    drawing_approval_date: Optional[date] = None
    drawing_number: Optional[str] = None
    drawing_initial_version: Optional[str] = None
    drawing_current_version: Optional[str] = None
    drawing_number_revised: Optional[str] = None

    remarks: Optional[str] = None


# -------------------------
# Create
# -------------------------

class OrderDetailCreate(OrderDetailBase):
    pass


# -------------------------
# Update
# -------------------------

class OrderDetailUpdate(BaseModel):
    company_id: Optional[int] = None
    tender_id: Optional[int] = None
    po_number: Optional[str] = None
    order_description: Optional[str] = None
    order_date: Optional[date] = None
    po_commencemnt_date: Optional[date] = None

    order_value: OptionalDecimal14_4 = None
    currency: Optional[CurrencyEnum] = None
    order_value_aed: OptionalDecimal14_4 = None
    revised_value_lme: OptionalDecimal14_4 = None
    revised_value_lme_aed: OptionalDecimal14_4 = None

    kka_commission_percent: OptionalPercent5_2 = None

    old_po_id: Optional[int] = None
    no_of_consignments: Optional[int] = None

    order_confirmation_no: Optional[str] = None
    order_confirmation_letter_ref: Optional[str] = None
    order_confirmation_date: Optional[date] = None
    po_confirmation_date_srm: Optional[date] = None

    last_contractual_delivery: Optional[date] = None
    actual_last_delivery: Optional[date] = None

    drawing_submission_date: Optional[date] = None
    drawing_approval_date: Optional[date] = None
    drawing_number: Optional[str] = None
    drawing_initial_version: Optional[str] = None
    drawing_current_version: Optional[str] = None
    drawing_number_revised: Optional[str] = None

    remarks: Optional[str] = None


# -------------------------
# Read
# -------------------------

class OrderDetailRead(OrderDetailBase):
    order_id: int

    class Config:
        from_attributes = True
