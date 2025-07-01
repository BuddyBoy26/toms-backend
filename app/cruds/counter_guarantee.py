from sqlalchemy.orm import Session
from app.models.counter_guarantee import CounterGuarantee, GuaranteeTypeEnum
from app.schemas.counter_guarantee import (
    CounterGuaranteeCreate,
    CounterGuaranteeUpdate,
)

def get_counter_guarantees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CounterGuarantee).offset(skip).limit(limit).all()

def get_counter_guarantee(db: Session, cg_id: int):
    return (
        db.query(CounterGuarantee)
        .filter(CounterGuarantee.cg_id == cg_id)
        .first()
    )

def create_counter_guarantee(db: Session, in_cg: CounterGuaranteeCreate):
    db_obj = CounterGuarantee(**in_cg.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_counter_guarantee(db: Session, cg_id: int, in_cg: CounterGuaranteeUpdate):
    obj = get_counter_guarantee(db, cg_id)
    if not obj:
        return None
    for field, value in in_cg.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_counter_guarantee(db: Session, cg_id: int):
    obj = get_counter_guarantee(db, cg_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

def list_ref_numbers_by_type(db: Session, guarantee_type: GuaranteeTypeEnum) -> List[str]:
    """
    Return all guarantee_ref_number values for a given type.
    """
    rows = (
        db.query(CounterGuarantee.guarantee_ref_number)
          .filter(CounterGuarantee.guarantee_type == guarantee_type)
          .order_by(CounterGuarantee.guarantee_ref_number)
          .all()
    )
    # unpack list of 1-tuples to list of strings
    return [r[0] for r in rows]
