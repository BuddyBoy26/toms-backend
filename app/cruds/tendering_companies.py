from sqlalchemy.orm import Session
from app.models.tendering_companies import TenderingCompanies
from app.schemas.tendering_companies import (
    TenderingCompaniesCreate,
    TenderingCompaniesUpdate,
)

BOOL_FIELDS = [
    "tender_bought", "participated", "result_saved",
    "evaluations_received", "memo", "po_copies",
]

def _bool_to_int(v):
    if v is None:
        return None
    return 1 if v else 0

def get_tendering_entries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TenderingCompanies).offset(skip).limit(limit).all()

def get_tendering_entry(db: Session, tc_id: int):
    return db.query(TenderingCompanies).filter(
        TenderingCompanies.tendering_companies_id == tc_id
    ).first()

def create_tendering_entry(db: Session, data: TenderingCompaniesCreate):
    # Convert booleans to 0/1 if needed
    payload = data.dict()
    for k in BOOL_FIELDS:
        payload[k] = _bool_to_int(payload.get(k, False))
    obj = TenderingCompanies(**payload)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_tendering_entry(db: Session, tc_id: int, data: TenderingCompaniesUpdate):
    obj = get_tendering_entry(db, tc_id)
    if not obj:
        return None
    changes = data.dict(exclude_unset=True)
    for k in BOOL_FIELDS:
        if k in changes and changes[k] is not None:
            changes[k] = _bool_to_int(changes[k])
    for field, value in changes.items():
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
