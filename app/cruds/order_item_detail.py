from sqlalchemy.orm import Session
from decimal import Decimal
from app.models.order_item_detail import OrderItemDetail
from app.cruds.order_detail import get_order
from app.cruds.item_master import get_item

from app.schemas.order_item_detail import (
    OrderItemDetailCreate,
    OrderItemDetailUpdate,
)

def get_order_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(OrderItemDetail).offset(skip).limit(limit).all()

def get_order_item(db: Session, oid: int):
    return (
        db.query(OrderItemDetail)
        .filter(OrderItemDetail.order_item_detail_id == oid)
        .first()
    )

def create_order_item(db: Session, in_o: OrderItemDetailCreate):
    # Ensure parent exists
    if not get_order(db, in_o.order_id):
        return None, "order_not_found"
    if not get_item(db, in_o.item_id):
        return None, "item_not_found"
    
    # Convert to dict
    data = in_o.dict()
    
    # CRITICAL FIX: Auto-calculate item_total_value if not provided
    # if data.get('item_total_value') is None:
    #     quantity = data.get('item_quantity')
    #     unit_price = data.get('item_unit_price')
        
    #     if quantity is not None and unit_price is not None:
    #         # Calculate: quantity * unit_price
    #         data['item_total_value'] = Decimal(str(quantity)) * Decimal(str(unit_price))
    #     else:
    #         # Fallback to 0 if we can't calculate
    #         data['item_total_value'] = Decimal('0')
    
    # Create the database object with calculated value
    db_obj = OrderItemDetail(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj, None

def update_order_item(db: Session, oid: int, in_o: OrderItemDetailUpdate):
    obj = get_order_item(db, oid)
    if not obj:
        return None
    
    # Update fields
    for field, value in in_o.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    
    # CRITICAL FIX: Recalculate item_total_value if quantity or unit_price changed
    # if obj.item_quantity is not None and obj.item_unit_price is not None:
    #     obj.item_total_value = Decimal(str(obj.item_quantity)) * Decimal(str(obj.item_unit_price))
    
    db.commit()
    db.refresh(obj)
    return obj

def delete_order_item(db: Session, oid: int):
    obj = get_order_item(db, oid)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj