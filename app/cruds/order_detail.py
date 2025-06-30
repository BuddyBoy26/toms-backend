from sqlalchemy.orm import Session
from app.models.order_detail import OrderDetail
from app.schemas.order_detail import OrderDetailCreate, OrderDetailUpdate

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(OrderDetail).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int):
    return db.query(OrderDetail).filter(OrderDetail.order_id == order_id).first()

def create_order(db: Session, in_o: OrderDetailCreate):
    db_obj = OrderDetail(**in_o.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_order(db: Session, oid: int, in_o: OrderDetailUpdate):
    obj = get_order(db, oid)
    if not obj:
        return None
    for field, value in in_o.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_order(db: Session, oid: int):
    obj = get_order(db, oid)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
