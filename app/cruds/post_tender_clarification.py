from sqlalchemy.orm import Session
from datetime import date
from app.models.post_tender_clarification import PostTenderClarification
from app.schemas.post_tender_clarification import (
    PostTenderClarificationCreate,
    PostTenderClarificationUpdate,
)
from app.cruds.tender import get_tender
from app.cruds.company_master import get_company

def get_ptcs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PostTenderClarification).offset(skip).limit(limit).all()

def get_ptc(db: Session, ptc_id: int):
    return (
        db.query(PostTenderClarification)
          .filter(PostTenderClarification.ptc_id == ptc_id)
          .first()
    )

def create_ptc(db: Session, in_ptc: PostTenderClarificationCreate):
    # FK checks
    if not get_tender(db, in_ptc.tender_id):
        return None, "tender_not_found"
    if not get_company(db, in_ptc.company_id):
        return None, "company_not_found"
    db_obj = PostTenderClarification(**in_ptc.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj, None

def update_ptc(db: Session, ptc_id: int, in_ptc: PostTenderClarificationUpdate):
    obj = get_ptc(db, ptc_id)
    if not obj:
        return None
    for field, value in in_ptc.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_ptc(db: Session, ptc_id: int):
    obj = get_ptc(db, ptc_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

def list_outstanding_ptcs(db: Session):
    today = date.today()
    return (
        db.query(PostTenderClarification)
          .filter(
              PostTenderClarification.ptc_reply_submission_date.is_(None),
              PostTenderClarification.ptc_reply_required_by <= today
          )
          .all()
    )
