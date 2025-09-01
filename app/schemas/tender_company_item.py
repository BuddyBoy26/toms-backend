from pydantic import BaseModel, Field
from typing import Optional, Annotated
from decimal import Decimal

Decimal12 = Annotated[Decimal, Field(..., max_digits=12, decimal_places=2)]
Decimal5_2 = Annotated[Decimal, Field(..., max_digits=5, decimal_places=2)]

class TenderCompanyItemBase(BaseModel):
    tendering_companies_id: int
    item_id: int               # internal (FK to item_master.item_no)
    item_no_dewa: str          # shown to DEWA/users
    item_price: Decimal12
    discount_percent: Decimal5_2

class TenderCompanyItemCreate(TenderCompanyItemBase):
    pass

class TenderCompanyItemUpdate(BaseModel):
    # All optional for PATCH
    tendering_companies_id: Optional[int] = None
    item_id: Optional[int] = None
    item_no_dewa: Optional[str] = None
    item_price: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    discount_percent: Optional[Decimal] = Field(None, max_digits=5, decimal_places=2)

class TenderCompanyItemRead(TenderCompanyItemBase):
    id: int

    class Config:
        from_attributes = True
