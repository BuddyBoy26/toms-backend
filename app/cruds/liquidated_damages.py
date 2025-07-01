from sqlalchemy.orm import Session
from app.models.liquidated_damages import LiquidatedDamages
from app.schemas.liquidated_damages import (
    LiquidatedDamagesCreate,
    LiquidatedDamagesUpdate,
)
from app.cruds.lot_monitoring import get_lot

def get_liquidated_damages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LiquidatedDamages).offset(skip).limit(limit).all()

def get_liquidated_damage(db: Session, ld_id: int):
    return (
        db.query(LiquidatedDamages)
        .filter(LiquidatedDamages.ld_id == ld_id)
        .first()
    )

def create_liquidated_damage(db: Session, in_ld: LiquidatedDamagesCreate):
    if not get_lot(db, in_ld.lot_id):
        return None, "lot_not_found"
    db_obj = LiquidatedDamages(**in_ld.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj, None

def update_liquidated_damage(db: Session, ld_id: int, in_ld: LiquidatedDamagesUpdate):
    obj = get_liquidated_damage(db, ld_id)
    if not obj:
        return None
    for field, value in in_ld.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_liquidated_damage(db: Session, ld_id: int):
    obj = get_liquidated_damage(db, ld_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
