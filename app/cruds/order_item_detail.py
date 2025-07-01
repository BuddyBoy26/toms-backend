from sqlalchemy.orm import Session
from app.models.order_item_detail import OrderItemDetail
from app.cruds.order_detail    import get_order
from app.cruds.item_master     import get_item

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
    # ensure parent exists
    if not get_order(db, in_o.order_id):
        return None, "order_not_found"
    if not get_item(db, in_o.item_id):
        return None, "item_not_found"
    db_obj = OrderItemDetail(**in_o.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj, None

def update_order_item(db: Session, oid: int, in_o: OrderItemDetailUpdate):
    obj = get_order_item(db, oid)
    if not obj:
        return None
    for field, value in in_o.dict(exclude_unset=True).items():
        setattr(obj, field, value)
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
