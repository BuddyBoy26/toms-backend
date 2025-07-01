from sqlalchemy.orm import Session
from app.models.lot_monitoring import LotMonitoring
from app.cruds.order_item_detail import get_order_item

def get_lots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LotMonitoring).offset(skip).limit(limit).all()

def get_lot(db: Session, lot_id: str):
    return db.query(LotMonitoring).filter(LotMonitoring.lot_id == lot_id).first()

def create_lot(db: Session, in_lot: LotMonitoring):
    # check parent exists
    if not get_order_item(db, in_lot.order_item_detail_id):
        return None, "order_item_not_found"
    db.add(in_lot)
    db.commit()
    db.refresh(in_lot)
    return in_lot, None

def update_lot(db: Session, lot_id: str, data):
    obj = get_lot(db, lot_id)
    if not obj:
        return None
    for field, val in data.dict(exclude_unset=True).items():
        setattr(obj, field, val)
    db.commit()
    db.refresh(obj)
    return obj

def delete_lot(db: Session, lot_id: str):
    obj = get_lot(db, lot_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
