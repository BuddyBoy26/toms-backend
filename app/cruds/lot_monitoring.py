# app/cruds/lot_monitoring.py
from sqlalchemy.orm import Session
from app import models, schemas
from app.cruds.order_item_detail import get_order_item

def get_lots(db: Session, skip: int = 0, limit: int = 100):
    # query the ORM model
    return db.query(models.LotMonitoring) \
             .offset(skip) \
             .limit(limit) \
             .all()

def get_lot(db: Session, lot_id: str):
    return db.query(models.LotMonitoring) \
             .filter(models.LotMonitoring.lot_id == lot_id) \
             .first()

def create_lot(db: Session, in_lot: schemas.LotMonitoringCreate):
    if not get_order_item(db, in_lot.order_item_detail_id):
        return None, "order_item_not_found"

    db_lot = models.LotMonitoring(**in_lot.dict())
    db.add(db_lot)
    db.commit()
    db.refresh(db_lot)
    return db_lot, None

def update_lot(db: Session, lot_id: str, data: schemas.LotMonitoringUpdate):
    db_lot = get_lot(db, lot_id)
    if not db_lot:
        return None

    for field, val in data.dict(exclude_unset=True).items():
        setattr(db_lot, field, val)

    db.commit()
    db.refresh(db_lot)
    return db_lot

def delete_lot(db: Session, lot_id: str):
    db_lot = get_lot(db, lot_id)
    if not db_lot:
        return None

    db.delete(db_lot)
    db.commit()
    return db_lot
