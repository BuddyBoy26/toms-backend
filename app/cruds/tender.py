from sqlalchemy.orm import Session
from passlib.context import CryptContext
import app.models as models
from app.schemas import  TenderCreate, TenderBase

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_tenders(db: Session, skip=0, limit=100):
    return db.query(models.Tender).offset(skip).limit(limit).all()

def get_tender(db: Session, tender_id: int):
    return db.query(models.Tender).filter(models.Tender.id == tender_id).first()

def create_tender(db: Session, in_t: TenderCreate, creator_id: int):
    db_obj = models.Tender(**in_t.dict(), created_by_id=creator_id)
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj

def update_tender(db: Session, tid: int, in_t: TenderBase):
    obj = get_tender(db, tid)
    if not obj: return None
    for k, v in in_t.dict().items(): setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

def delete_tender(db: Session, tid: int):
    obj = get_tender(db, tid)
    if not obj: return None
    db.delete(obj); db.commit()
    return obj
