from sqlalchemy.orm import Session
from app.models.tender_company_item import TenderCompanyItem
from app.cruds.tendering_companies import get_tendering_entry
from app.schemas.tender_company_item import (
    TenderCompanyItemCreate,
    TenderCompanyItemUpdate,
)

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TenderCompanyItem).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return (
        db.query(TenderCompanyItem)
        .filter(TenderCompanyItem.id == item_id)
        .first()
    )

def create_item(db: Session, in_i: TenderCompanyItemCreate):
    parent = get_tendering_entry(db, in_i.tendering_companies_id)
    if not parent:
        return None, "parent_not_found"
    # default discount to parent's if not provided
    dp = in_i.discount_percent if in_i.discount_percent is not None else parent.discount_percent
    db_obj = TenderCompanyItem(
        **in_i.dict(exclude={"discount_percent"}),
        discount_percent=dp
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj, None

def update_item(db: Session, iid: int, in_i: TenderCompanyItemUpdate):
    obj = get_item(db, iid)
    if not obj:
        return None
    for field, value in in_i.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_item(db: Session, iid: int):
    obj = get_item(db, iid)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
