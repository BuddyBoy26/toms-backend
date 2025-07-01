from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class OrderEventBase(BaseModel):
    order_id: int
    date: date = Field(..., example="2025-07-20")
    event: str = Field(..., example="PO received")
    remarks: Optional[str] = Field(None, example="Delivered to warehouse")

class OrderEventCreate(OrderEventBase):
    """All fields except auto‐PK"""

class OrderEventUpdate(BaseModel):
    date: Optional[date] = None
    event: Optional[str] = None
    remarks: Optional[str] = None

class OrderEventRead(OrderEventBase):
    order_event_id: int

    class Config:
        from_attributes = True
