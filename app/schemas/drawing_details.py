from pydantic import BaseModel, Field, constr
from datetime import date
from typing import Optional

class DrawingDetailsBase(BaseModel):
    drawing_no: str = Field(strip_whitespace=True)
    drawing_version: Optional[str] = None
    submission_date: Optional[date] = None
    revision: Optional[str] = None
    approval_date: Optional[date] = None
    sent_date: Optional[date] = None

class DrawingDetailsCreate(DrawingDetailsBase):
    tender_no: str = Field(strip_whitespace=True)
    order_id: int = Field(strip_whitespace=True)

class DrawingDetailsRead(DrawingDetailsBase):
    id: int
    tender_no: str
    order_id: int

    class Config:
        from_attributes = True
