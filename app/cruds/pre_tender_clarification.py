from sqlalchemy.orm import Session
from datetime import date
from app.models.pre_tender_clarification import PreTenderClarification
from app.schemas.pre_tender_clarification import (
    PreTenderClarificationCreate,
    PreTenderClarificationUpdate,
)
from app.cruds.tendering_companies import get_tendering_entry

def get_pre_ptcs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PreTenderClarification).offset(skip).limit(limit).all()

def get_pre_ptc(db: Session, ptc_id: int):
    return (
        db.query(PreTenderClarification)
          .filter(PreTenderClarification.pre_ptc_id == ptc_id)
          .first()
    )

def create_pre_ptc(
    db: Session,
    in_ptc: PreTenderClarificationCreate
):
    # ensure the tender+company entry exists
    tc = get_tendering_entry(db, in_ptc.tender_id, in_ptc.company_id)
    if not tc:
        return None, "tendering_company_not_found"
    db_obj = PreTenderClarification(**in_ptc.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj, None

def update_pre_ptc(db: Session, ptc_id: int, in_ptc: PreTenderClarificationUpdate):
    obj = get_pre_ptc(db, ptc_id)
    if not obj:
        return None
    for field, value in in_ptc.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_pre_ptc(db: Session, ptc_id: int):
    obj = get_pre_ptc(db, ptc_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

def list_outstanding_pre_ptcs(db: Session):
    today = date.today()
    return (
        db.query(PreTenderClarification)
          .filter(
              PreTenderClarification.pre_ptc_reply_submission_date.is_(None),
              PreTenderClarification.pre_ptc_reply_required_by <= today
          )
          .all()
    )
