from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class LiquidatedDamagesBase(BaseModel):
    lot_id: str
    lot_qty: int
    actual_delivery_date: Optional[date] = None
    quantities_delivered: List[int] = Field(..., example=[45, 3, 2])
    delivery_delays_days: List[int] = Field(..., example=[0, 10, 20])

class LiquidatedDamagesCreate(LiquidatedDamagesBase):
    """All fields except auto‐PK."""

class LiquidatedDamagesUpdate(BaseModel):
    lot_qty: Optional[int] = None
    actual_delivery_date: Optional[date] = None
    quantities_delivered: Optional[List[int]] = None
    delivery_delays_days: Optional[List[int]] = None

class LiquidatedDamagesRead(LiquidatedDamagesBase):
    ld_id: int

    class Config:
        from_attributes = True
