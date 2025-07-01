from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PostTenderClarificationBase(BaseModel):
    tender_id: int
    company_id: int
    ptc_no: int = Field(..., example=1)
    ptc_ref_no: str = Field(..., example="MD-VPCN-11511-2024")
    ptc_date: date = Field(..., example="2024-12-06")
    ptc_received_date: date = Field(..., example="2024-12-10")
    ptc_reply_required_by: date = Field(..., example="2024-12-13")
    ptc_reply_submission_date: Optional[date] = Field(None, example="2024-12-12")

class PostTenderClarificationCreate(PostTenderClarificationBase):
    """All fields except auto PK."""

class PostTenderClarificationUpdate(BaseModel):
    ptc_ref_no: Optional[str] = None
    ptc_date: Optional[date] = None
    ptc_received_date: Optional[date] = None
    ptc_reply_required_by: Optional[date] = None
    ptc_reply_submission_date: Optional[date] = None

class PostTenderClarificationRead(PostTenderClarificationBase):
    ptc_id: int

    class Config:
        from_attributes = True
