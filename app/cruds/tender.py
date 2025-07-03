# app/cruds/tender.py

from sqlalchemy.orm import Session
from app.models.tender import Tender
from app.schemas.tender import TenderCreate, TenderUpdate

def get_tenders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tender).offset(skip).limit(limit).all()

def get_tender(db: Session, tender_id: int):
    return db.query(Tender).filter(Tender.tender_id == tender_id).first()

# ← NEW: lookup by tender_no (string)
def get_tender_by_no(db: Session, tender_no: str):
    return db.query(Tender).filter(Tender.tender_no == tender_no).first()

def create_tender(db: Session, in_t: TenderCreate):
    # ← enforce uniqueness on tender_no
    if get_tender_by_no(db, in_t.tender_no):
        # you can raise here or return None and handle in your router
        return None

    db_obj = Tender(**in_t.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_tender(db: Session, tender_id: int, in_t: TenderUpdate):
    obj = get_tender(db, tender_id)
    if not obj:
        return None
    for field, value in in_t.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_tender(db: Session, tender_id: int):
    obj = get_tender(db, tender_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
