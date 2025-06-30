from sqlalchemy.orm import Session
from app.models.product_master import ProductMaster
from app.schemas.product_master import (
    ProductMasterCreate,
    ProductMasterUpdate,
)

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductMaster).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return (
        db.query(ProductMaster)
        .filter(ProductMaster.product_id == product_id)
        .first()
    )

def create_product(db: Session, in_p: ProductMasterCreate):
    db_obj = ProductMaster(**in_p.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_product(db: Session, pid: int, in_p: ProductMasterUpdate):
    obj = get_product(db, pid)
    if not obj:
        return None
    for field, value in in_p.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_product(db: Session, pid: int):
    obj = get_product(db, pid)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
