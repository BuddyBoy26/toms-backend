from sqlalchemy.orm import Session
from app.models.item_master import ItemMaster
from app.schemas.item_master import (
    ItemMasterCreate,
    ItemMasterUpdate,
)

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ItemMaster).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return (
        db.query(ItemMaster)
        .filter(ItemMaster.item_id == item_id)
        .first()
    )

def create_item(db: Session, in_i: ItemMasterCreate):
    db_obj = ItemMaster(**in_i.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_item(db: Session, iid: int, in_i: ItemMasterUpdate):
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
