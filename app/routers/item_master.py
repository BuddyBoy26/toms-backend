from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.cruds.item_master as cruds
import app.schemas.item_master as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User
from app.cruds.product_master import get_product

router = APIRouter(prefix="/items", tags=["items"])

@router.get(
    "/",
    response_model=list[schemas.ItemMasterRead],
    summary="List items (auth required)",
)
def list_items(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_items(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.ItemMasterRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item (auth required)",
)
def create_item(
    i: schemas.ItemMasterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ensure the referenced product exists
    if not get_product(db, i.product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return cruds.create_item(db, i)

@router.get(
    "/{iid}",
    response_model=schemas.ItemMasterRead,
    summary="Get an item by ID (auth required)",
)
def read_item(
    iid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_item(db, iid)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    return obj

@router.put(
    "/{iid}",
    response_model=schemas.ItemMasterRead,
    summary="Replace an item (auth required)",
)
def replace_item(
    iid: int,
    i: schemas.ItemMasterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_item(db, iid)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    if not get_product(db, i.product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    obj.product_id = i.product_id
    obj.item_description = i.item_description
    obj.hs_code = i.hs_code
    db.commit()
    db.refresh(obj)
    return obj

@router.patch(
    "/{iid}",
    response_model=schemas.ItemMasterRead,
    summary="Update an item (partial, auth required)",
)
def update_item(
    iid: int,
    i: schemas.ItemMasterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if i.product_id is not None and not get_product(db, i.product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    obj = cruds.update_item(db, iid, i)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    return obj

@router.delete(
    "/{iid}",
    response_model=schemas.ItemMasterRead,
    summary="Delete an item (auth required)",
)
def delete_item(
    iid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_item(db, iid)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    return obj
