from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PreTenderClarificationBase(BaseModel):
    tender_id: int
    company_id: int
    pre_ptc_no: int = Field(..., example=1)
    pre_ptc_ref_no: str = Field(..., example="MD-VPCN-11511-2024")
    pre_ptc_date: date = Field(..., example="2024-12-06")
    pre_ptc_received_date: date = Field(..., example="2024-12-10")
    pre_ptc_reply_required_by: date = Field(..., example="2024-12-13")
    pre_ptc_reply_submission_date: Optional[date] = Field(None, example="2024-12-12")

class PreTenderClarificationCreate(PreTenderClarificationBase):
    """All fields except auto‐PK."""

class PreTenderClarificationUpdate(BaseModel):
    pre_ptc_ref_no: Optional[str] = None
    pre_ptc_date: Optional[date] = None
    pre_ptc_received_date: Optional[date] = None
    pre_ptc_reply_required_by: Optional[date] = None
    pre_ptc_reply_submission_date: Optional[date] = None

class PreTenderClarificationRead(PreTenderClarificationBase):
    pre_ptc_id: int

    class Config:
        from_attributes = True
