from pydantic import BaseModel, Field
from typing import Optional, Annotated
from decimal import Decimal

Decimal12 = Annotated[Decimal, Field(..., max_digits=12, decimal_places=2)]
OptionalDecimal12 = Optional[Annotated[Decimal, Field(None, max_digits=12, decimal_places=2)]]
Decimal5_2 = Annotated[Decimal, Field(..., max_digits=5, decimal_places=2)]
OptionalDecimal5_2 = Optional[Annotated[Decimal, Field(None, max_digits=5, decimal_places=2)]]

class TenderCompanyItemBase(BaseModel):
    tendering_companies_id: int
    item_id: int                # FK to item_master.item_id
    item_no_dewa: str           # DEWA-facing item reference
    item_price: Decimal12
    item_quantity: Decimal12
    item_total_value: Decimal12
    currency: str               # e.g., "AED", "USD", "EUR"
    discount_percent: OptionalDecimal5_2 = None
    discount_amount: OptionalDecimal12 = None
    discount_value: OptionalDecimal12 = None

class TenderCompanyItemCreate(TenderCompanyItemBase):
    pass

class TenderCompanyItemUpdate(BaseModel):
    # All optional for PATCH
    tendering_companies_id: Optional[int] = None
    item_id: Optional[int] = None
    item_no_dewa: Optional[str] = None
    item_price: OptionalDecimal12 = None
    item_quantity: OptionalDecimal12 = None
    item_total_value: OptionalDecimal12 = None
    currency: Optional[str] = None
    discount_percent: OptionalDecimal5_2 = None
    discount_amount: OptionalDecimal12 = None
    discount_value: OptionalDecimal12 = None

class TenderCompanyItemRead(TenderCompanyItemBase):
    id: int

    class Config:
        from_attributes = True