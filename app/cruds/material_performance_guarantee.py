from sqlalchemy.orm import Session
from app.models.material_performance_guarantee import MaterialPerformanceGuarantee
from app.schemas.material_performance_guarantee import (
    MaterialPerformanceGuaranteeCreate,
    MaterialPerformanceGuaranteeUpdate,
)
from app.cruds.order_detail import get_order

def get_material_performance_guarantees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MaterialPerformanceGuarantee).offset(skip).limit(limit).all()

def get_material_performance_guarantee(db: Session, mpg_id: int):
    return (
        db.query(MaterialPerformanceGuarantee)
        .filter(MaterialPerformanceGuarantee.mpg_id == mpg_id)
        .first()
    )

def create_material_performance_guarantee(db: Session, in_mpg: MaterialPerformanceGuaranteeCreate):
    if not get_order(db, in_mpg.order_id):
        return None, "order_not_found"
    db_obj = MaterialPerformanceGuarantee(**in_mpg.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj, None

def update_material_performance_guarantee(db: Session, mpg_id: int, in_mpg: MaterialPerformanceGuaranteeUpdate):
    obj = get_material_performance_guarantee(db, mpg_id)
    if not obj:
        return None
    for field, value in in_mpg.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_material_performance_guarantee(db: Session, mpg_id: int):
    obj = get_material_performance_guarantee(db, mpg_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
