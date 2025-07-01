from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from decimal import Decimal

# Constrained decimal for prices
Price = Annotated[Decimal, Field(..., max_digits=14, decimal_places=2)]

class OrderItemDetailBase(BaseModel):
    order_id: int
    item_id: int
    item_description: Optional[str] = None
    item_no_dewa: str
    item_quantity: int
    item_unit_price: Price
    number_of_lots: int

class OrderItemDetailCreate(OrderItemDetailBase):
    """All fields required except PK."""

class OrderItemDetailUpdate(BaseModel):
    item_description: Optional[str] = None
    item_no_dewa: Optional[str] = None
    item_quantity: Optional[int] = None
    item_unit_price: Optional[Price] = None
    number_of_lots: Optional[int] = None

class OrderItemDetailRead(OrderItemDetailBase):
    order_item_detail_id: int

    class Config:
        from_attributes = True
