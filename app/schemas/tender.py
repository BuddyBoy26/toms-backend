from pydantic import BaseModel, EmailStr
from fastapi import Depends, HTTPException, status
from datetime import datetime

class TenderBase(BaseModel):
    title: str
    description: str | None = None

class TenderCreate(TenderBase):
    pass

class TenderRead(TenderBase):
    id: int
    created_at: datetime
    created_by_id: int

    class Config:
        from_attributes = True