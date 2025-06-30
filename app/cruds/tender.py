from sqlalchemy.orm import Session
from app.models.tender import Tender
from app.schemas.tender import TenderCreate, TenderUpdate

def get_tenders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tender).offset(skip).limit(limit).all()

def get_tender(db: Session, tender_no: str):
    return db.query(Tender).filter(Tender.tender_no == tender_no).first()

def create_tender(db: Session, in_t: TenderCreate):
    db_obj = Tender(**in_t.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_tender(db: Session, tno: str, in_t: TenderUpdate):
    obj = get_tender(db, tno)
    if not obj:
        return None
    for field, value in in_t.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_tender(db: Session, tno: str):
    obj = get_tender(db, tno)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
