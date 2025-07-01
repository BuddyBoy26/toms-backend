from sqlalchemy.orm import Session
from app.models.performance_guarantee import PerformanceGuarantee
from app.schemas.performance_guarantee import (
    PerformanceGuaranteeCreate,
    PerformanceGuaranteeUpdate,
)
from app.cruds.order_detail import get_order

def get_performance_guarantees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PerformanceGuarantee).offset(skip).limit(limit).all()

def get_performance_guarantee(db: Session, pg_id: int):
    return (
        db.query(PerformanceGuarantee)
        .filter(PerformanceGuarantee.pg_id == pg_id)
        .first()
    )

def create_performance_guarantee(
    db: Session,
    in_pg: PerformanceGuaranteeCreate
):
    if not get_order(db, in_pg.order_id):
        return None, "order_not_found"
    db_obj = PerformanceGuarantee(**in_pg.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj, None

def update_performance_guarantee(
    db: Session,
    pg_id: int,
    in_pg: PerformanceGuaranteeUpdate
):
    obj = get_performance_guarantee(db, pg_id)
    if not obj:
        return None
    for field, value in in_pg.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_performance_guarantee(db: Session, pg_id: int):
    obj = get_performance_guarantee(db, pg_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
