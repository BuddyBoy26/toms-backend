from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EventBase(BaseModel):
    description: str = Field(..., example="Tesar Meeting with DEWA")
    start_dt: datetime = Field(..., example="2025-07-15T10:30:00")
    end_dt:   datetime = Field(..., example="2025-07-15T12:00:00")
    remarks:  Optional[str] = Field(None, example="Col's Internal arc test")

class EventCreate(EventBase):
    """Client supplies all but event_id."""

class EventUpdate(BaseModel):
    description: Optional[str] = None
    start_dt:    Optional[datetime] = None
    end_dt:      Optional[datetime] = None
    remarks:     Optional[str] = None

class EventRead(EventBase):
    event_id: int

    class Config:
        from_attributes = True
