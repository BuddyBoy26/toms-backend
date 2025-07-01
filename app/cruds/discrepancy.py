from sqlalchemy.orm import Session
from app.models.discrepancy import Discrepancy
from app.schemas.discrepancy import DiscrepancyCreate, DiscrepancyUpdate
from app.cruds.lot_monitoring import get_lot

def get_discrepancies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Discrepancy).offset(skip).limit(limit).all()

def get_discrepancy(db: Session, did: int):
    return (
        db.query(Discrepancy)
        .filter(Discrepancy.discrepancy_id == did)
        .first()
    )

def create_discrepancy(db: Session, in_d: DiscrepancyCreate):
    if not get_lot(db, in_d.lot_id):
        return None, "lot_not_found"
    db_obj = Discrepancy(**in_d.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj, None

def update_discrepancy(db: Session, did: int, in_d: DiscrepancyUpdate):
    obj = get_discrepancy(db, did)
    if not obj:
        return None
    for field, value in in_d.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_discrepancy(db: Session, did: int):
    obj = get_discrepancy(db, did)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
