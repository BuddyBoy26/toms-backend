# app/schemas/tender.py

from pydantic import BaseModel, Field
from typing import Optional, Annotated
from decimal import Decimal
from datetime import date

# Define an Annotated type for a 12-digit, 2-decimal Decimal
Decimal12 = Annotated[
    Decimal,
    Field(..., max_digits=12, decimal_places=2)
]
# And an optional version
OptionalDecimal12 = Optional[
    Annotated[Decimal, Field(None, max_digits=12, decimal_places=2)]
]

class TenderBase(BaseModel):
    tender_description: str
    tender_date: date
    closing_date: date
    tender_fees: Decimal12
    bond_guarantee_amt: OptionalDecimal12 = None

class TenderCreate(TenderBase):
    tender_no: str  # client-supplied PK

class TenderUpdate(BaseModel):
    tender_description: Optional[str] = None
    tender_date: Optional[date] = None
    closing_date: Optional[date] = None
    tender_fees: OptionalDecimal12 = None
    bond_guarantee_amt: OptionalDecimal12 = None

class TenderRead(TenderBase):
    tender_id: int  
    tender_no: str

    class Config:
        from_attributes = True
