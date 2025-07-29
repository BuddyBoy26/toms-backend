from sqlalchemy.orm import Session
from datetime import date
from app.models.post_tender_clarification import PostTenderClarification
from app.schemas.post_tender_clarification import (
    PostTenderClarificationCreate,
    PostTenderClarificationUpdate,
)
from app.cruds.tendering_companies import get_tendering_entry

def get_post_tender_clarifications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PostTenderClarification).offset(skip).limit(limit).all()

def get_post_tender_clarification(db: Session, ptc_id: int):
    return (
        db.query(PostTenderClarification)
          .filter(PostTenderClarification.ptc_id == ptc_id)
          .first()
    )

def create_post_tender_clarification(db: Session, in_ptc: PostTenderClarificationCreate):
    # FK checks
    tc = get_tendering_entry(db, in_ptc.tc_id)
    db_obj = PostTenderClarification(**in_ptc.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj, None

def update_post_tender_clarification(db: Session, ptc_id: int, in_ptc: PostTenderClarificationUpdate):
    obj = get_post_tender_clarification(db, ptc_id)
    if not obj:
        return None
    for field, value in in_ptc.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_post_tender_clarification(db: Session, ptc_id: int):
    obj = get_post_tender_clarification(db, ptc_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

def list_outstanding_post_tender_clarifications(db: Session):
    today = date.today()
    return (
        db.query(PostTenderClarification)
          .filter(
              PostTenderClarification.ptc_reply_submission_date.is_(None),
              PostTenderClarification.ptc_reply_required_by <= today
          )
          .all()
    )
