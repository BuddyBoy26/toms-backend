from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from decimal import Decimal

# Constrained decimal for percentages (0–100 with two decimals)
Percent = Annotated[Decimal, Field(..., ge=0, le=100, decimal_places=2)]
OptionalPercent = Optional[Annotated[Decimal, Field(None, ge=0, le=100, decimal_places=2)]]

class TenderCompanyItemBase(BaseModel):
    tendering_companies_id: int
    item_no_dewa: str
    discount_percent: OptionalPercent = None

class TenderCompanyItemCreate(TenderCompanyItemBase):
    """If discount_percent is None, will default from parent."""

class TenderCompanyItemUpdate(BaseModel):
    item_no_dewa: Optional[str] = None
    discount_percent: OptionalPercent = None

class TenderCompanyItemRead(TenderCompanyItemBase):
    id: int
    discount_percent: Percent  # always set when reading

    class Config:
        from_attributes = True
