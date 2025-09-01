from sqlalchemy.orm import Session
from app.models.company_master import CompanyMaster
from app.models.product_master import ProductMaster
from app.schemas.company_master import (
    CompanyMasterCreate,
    CompanyMasterUpdate,
)

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CompanyMaster).offset(skip).limit(limit).all()

def get_company(db: Session, company_id: int):
    return (
        db.query(CompanyMaster)
        .filter(CompanyMaster.company_id == company_id)
        .first()
    )

def create_company(db: Session, in_c: CompanyMasterCreate):
    # Extract product_ids separately
    data = in_c.dict()
    product_ids = data.pop("product_ids", [])

    db_obj = CompanyMaster(**data)

    if product_ids:
        products = db.query(ProductMaster).filter(ProductMaster.product_id.in_(product_ids)).all()
        db_obj.products = products

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_company(db: Session, cid: int, in_c: CompanyMasterUpdate):
    obj = get_company(db, cid)
    if not obj:
        return None

    data = in_c.dict(exclude_unset=True)
    product_ids = data.pop("product_ids", None)

    # Update scalar fields
    for field, value in data.items():
        setattr(obj, field, value)

    # Update relationships if provided
    if product_ids is not None:
        products = db.query(ProductMaster).filter(ProductMaster.product_id.in_(product_ids)).all()
        obj.products = products

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
