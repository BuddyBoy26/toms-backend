from sqlalchemy.orm import Session
from app.models.delivery_procedure import DeliveryProcedure
from app.schemas.delivery_procedure import (
    DeliveryProcedureCreate,
    DeliveryProcedureUpdate,
)
from app.cruds.lot_monitoring import get_lot
from app.cruds.order_item_detail import get_order_item

def get_delivery_procedures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DeliveryProcedure).offset(skip).limit(limit).all()

def get_delivery_procedure(db: Session, dp_id: int):
    return (
        db.query(DeliveryProcedure)
        .filter(DeliveryProcedure.dp_id == dp_id)
        .first()
    )

def create_delivery_procedure(db: Session, in_dp: DeliveryProcedureCreate):
    if not get_lot(db, in_dp.lot_id):
        return None, "lot_not_found"
    if not get_order_item(db, in_dp.order_item_detail_id):
        return None, "order_item_not_found"
    db_obj = DeliveryProcedure(**in_dp.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj, None

def update_delivery_procedure(db: Session, dp_id: int, in_dp: DeliveryProcedureUpdate):
    obj = get_delivery_procedure(db, dp_id)
    if not obj:
        return None
    for field, value in in_dp.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_delivery_procedure(db: Session, dp_id: int):
    obj = get_delivery_procedure(db, dp_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
