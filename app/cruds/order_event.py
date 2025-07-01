from sqlalchemy.orm import Session
from app.models.order_event import OrderEvent
from app.schemas.order_event import OrderEventCreate, OrderEventUpdate
from app.cruds.order_detail import get_order

def get_order_events(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(OrderEvent)
          .order_by(OrderEvent.date)
          .offset(skip)
          .limit(limit)
          .all()
    )

def get_order_event(db: Session, oe_id: int):
    return (
        db.query(OrderEvent)
          .filter(OrderEvent.order_event_id == oe_id)
          .first()
    )

def create_order_event(db: Session, in_ev: OrderEventCreate):
    if not get_order(db, in_ev.order_id):
        return None, "order_not_found"
    db_obj = OrderEvent(**in_ev.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj, None

def update_order_event(db: Session, oe_id: int, in_ev: OrderEventUpdate):
    obj = get_order_event(db, oe_id)
    if not obj:
        return None
    for field, value in in_ev.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_order_event(db: Session, oe_id: int):
    obj = get_order_event(db, oe_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
