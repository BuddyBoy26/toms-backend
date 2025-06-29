from sqlalchemy.orm import Session
from app.models.company_master import CompanyMaster
from app.schemas.company_master import CompanyMasterCreate, CompanyMasterUpdate

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CompanyMaster).offset(skip).limit(limit).all()

def get_company(db: Session, company_id: int):
    return (
        db.query(CompanyMaster)
        .filter(CompanyMaster.company_id == company_id)
        .first()
    )

def create_company(db: Session, in_c: CompanyMasterCreate):
    db_obj = CompanyMaster(**in_c.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_company(db: Session, cid: int, in_c: CompanyMasterUpdate):
    obj = get_company(db, cid)
    if not obj:
        return None
    for field, value in in_c.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_company(db: Session, cid: int):
    obj = get_company(db, cid)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
