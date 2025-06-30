from sqlalchemy.orm import Session
from app.models.tendering_companies import TenderingCompanies
from app.schemas.tendering_companies import (
    TenderingCompaniesCreate,
    TenderingCompaniesUpdate,
)

def get_tendering_entries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TenderingCompanies).offset(skip).limit(limit).all()

def get_tendering_entry(db: Session, tc_id: int):
    return (
        db.query(TenderingCompanies)
        .filter(TenderingCompanies.tendering_companies_id == tc_id)
        .first()
    )

def create_tendering_entry(db: Session, in_tc: TenderingCompaniesCreate):
    db_obj = TenderingCompanies(**in_tc.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_tendering_entry(db: Session, tc_id: int, in_tc: TenderingCompaniesUpdate):
    obj = get_tendering_entry(db, tc_id)
    if not obj:
        return None
    for field, value in in_tc.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_tendering_entry(db: Session, tc_id: int):
    obj = get_tendering_entry(db, tc_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
