# app/schemas/order_item_detail.py
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from decimal import Decimal

# Constrained decimals
Decimal14 = Annotated[Decimal, Field(max_digits=14, decimal_places=4)]
OptionalDecimal14 = Optional[Annotated[Decimal, Field(None, max_digits=14, decimal_places=4)]]

class OrderItemDetailBase(BaseModel):
    order_id: int
    item_id: int
    item_description: Optional[str] = None
    item_no_dewa: str
    item_quantity: Decimal14  # ✅ FIXED - Just use the type, no = Decimal
    item_unit_price: Decimal14  # ✅ FIXED
    currency: str
    number_of_lots: Optional[int] = None
    
    # Discount fields
    discount_percent: OptionalDecimal14 = None
    discount_amount: OptionalDecimal14 = None
    discount_value: OptionalDecimal14 = None

class OrderItemDetailCreate(OrderItemDetailBase):
    """All fields may be provided by client."""
    pass

class OrderItemDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    item_id: Optional[int] = None
    item_description: Optional[str] = None
    item_no_dewa: Optional[str] = None
    item_quantity: OptionalDecimal14 = None
    item_unit_price: OptionalDecimal14 = None
    currency: Optional[str] = None
    number_of_lots: Optional[int] = None
    
    # Discount fields
    discount_percent: OptionalDecimal14 = None
    discount_amount: OptionalDecimal14 = None
    discount_value: OptionalDecimal14 = None

class OrderItemDetailRead(OrderItemDetailBase):
    order_item_detail_id: int
    
    class Config:
        from_attributes = True