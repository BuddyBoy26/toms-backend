from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.tender_company_item import TenderCompanyItem
from app.cruds.tendering_companies import get_tendering_entry
from app.schemas.tender_company_item import (
    TenderCompanyItemCreate,
    TenderCompanyItemUpdate,
)

def get_tender_company_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TenderCompanyItem).offset(skip).limit(limit).all()

def get_tender_company_items_by_tendering_company(
    db: Session, 
    tendering_companies_id: int,
    skip: int = 0, 
    limit: int = 100
):
    """Get all items for a specific tendering company"""
    return (
        db.query(TenderCompanyItem)
        .filter(TenderCompanyItem.tendering_companies_id == tendering_companies_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_tender_company_item(db: Session, item_id: int):
    return (
        db.query(TenderCompanyItem)
        .filter(TenderCompanyItem.id == item_id)
        .first()
    )

def get_tender_company_item_by_unique_key(
    db: Session,
    tendering_companies_id: int,
    item_id: int
):
    return (
        db.query(TenderCompanyItem)
        .filter(
            TenderCompanyItem.tendering_companies_id == tendering_companies_id,
            TenderCompanyItem.item_id == item_id
        )
        .first()
    )

def create_tender_company_item(db: Session, in_i: TenderCompanyItemCreate):
    parent = get_tendering_entry(db, in_i.tendering_companies_id)
    if not parent:
        return None, "parent_not_found"

    dp = (
        in_i.discount_percent
        if in_i.discount_percent is not None
        else parent.discount_percent
    )

    existing = get_tender_company_item_by_unique_key(
        db,
        in_i.tendering_companies_id,
        in_i.item_id
    )

    # ✅ UPDATE if already exists (same tender + same item)
    if existing:
        for field, value in in_i.dict(exclude_unset=True).items():
            setattr(existing, field, value)

        # ensure discount default rule still applies
        if in_i.discount_percent is None:
            existing.discount_percent = dp

        db.commit()
        db.refresh(existing)
        return existing, None

    # ✅ INSERT if not exists
    db_obj = TenderCompanyItem(
        **in_i.dict(exclude={"discount_percent"}),
        discount_percent=dp
    )

    db.add(db_obj)

    try:
        db.commit()
        db.refresh(db_obj)
        return db_obj, None

    except IntegrityError:
        # safety fallback for race condition
        db.rollback()

        existing = get_tender_company_item_by_unique_key(
            db,
            in_i.tendering_companies_id,
            in_i.item_id
        )

        if existing:
            for field, value in in_i.dict(exclude_unset=True).items():
                setattr(existing, field, value)

            db.commit()
            db.refresh(existing)
            return existing, None

        return None, "integrity_error"
    
def update_tender_company_item(db: Session, iid: int, in_i: TenderCompanyItemUpdate):
    obj = get_tender_company_item(db, iid)
    if not obj:
        return None

    for field, value in in_i.dict(exclude_unset=True).items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj

def delete_tender_company_item(db: Session, iid: int):
    obj = get_tender_company_item(db, iid)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj