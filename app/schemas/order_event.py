from __future__ import annotations
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class OrderEventBase(BaseModel):
    order_id: int
    event_date: date = Field(..., example="2025-07-20")
    event: str      = Field(..., example="PO received")
    remarks: Optional[str] = Field(None, example="Delivered to warehouse")

class OrderEventCreate(OrderEventBase):
    """All fields required to create an OrderEvent"""

class OrderEventUpdate(BaseModel):
    """Fields allowed to update on an OrderEvent"""
    event_date: Optional[date] = None
    event: Optional[str]       = None
    remarks: Optional[str]     = None

class OrderEventRead(OrderEventBase):
    order_event_id: int

    # Pydantic-v2 way to enable ORM mode
    model_config = ConfigDict(from_attributes=True)
