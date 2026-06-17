from pydantic import BaseModel, Field
from typing import Optional, List, Annotated
from decimal import Decimal
from datetime import date

from app.models.tender import TenderType

Decimal12 = Annotated[Decimal, Field(..., max_digits=12, decimal_places=2)]
OptionalDecimal12 = Optional[Annotated[Decimal, Field(None, max_digits=12, decimal_places=2)]]

class TenderBase(BaseModel):
    tender_no: str
    tender_description: str
    tender_date: date                         # Invitation Date
    closing_date: Optional[date] = None       # Closing Date
    tender_fees: OptionalDecimal12 = None
    bond_guarantee_amt: OptionalDecimal12 = None
    tender_type: TenderType
    currency: Optional[str] = None

class TenderCreate(TenderBase):
    tender_no: str

class TenderUpdate(BaseModel):
    tender_no: Optional[str] = None
    tender_description: Optional[str] = None
    tender_date: Optional[date] = None
    closing_date: Optional[date] = None
    tender_fees: OptionalDecimal12 = None
    bond_guarantee_amt: OptionalDecimal12 = None
    tender_type: Optional[TenderType] = None
    # Only editable in the Edit page
    extension_dates: Optional[List[date]] = None
    currency: Optional[str] = None

class TenderRead(TenderBase):
    tender_id: int
    tender_no: str
    extension_dates: Optional[List[date]] = None

    class Config:
        from_attributes = True
