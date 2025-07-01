from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.cruds.order_item_detail as cruds
import app.schemas.order_item_detail as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/order-items", tags=["order-items"])

@router.get(
    "/",
    response_model=list[schemas.OrderItemDetailRead],
    summary="List order items (auth required)"
)
def list_order_items(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_order_items(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.OrderItemDetailRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an order item (auth required)"
)
def create_order_item(
    o: schemas.OrderItemDetailCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj, err = cruds.create_order_item(db, o)
    if err == "order_not_found":
        raise HTTPException(status_code=404, detail="Order not found")
    if err == "item_not_found":
        raise HTTPException(status_code=404, detail="Item not found")
    return obj

@router.get(
    "/{oid}",
    response_model=schemas.OrderItemDetailRead,
    summary="Get an order item (auth required)"
)
def read_order_item(
    oid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_order_item(db, oid)
    if not obj:
        raise HTTPException(status_code=404, detail="Order item not found")
    return obj

@router.put(
    "/{oid}",
    response_model=schemas.OrderItemDetailRead,
    summary="Replace an order item (auth required)"
)
def replace_order_item(
    oid: int,
    o: schemas.OrderItemDetailCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_order_item(db, oid)
    if not existing:
        raise HTTPException(status_code=404, detail="Order item not found")
    new_obj, err = cruds.create_order_item(db, o)
    if err:
        raise HTTPException(status_code=400, detail="Could not recreate order item")
    cruds.delete_order_item(db, oid)
    return new_obj

@router.patch(
    "/{oid}",
    response_model=schemas.OrderItemDetailRead,
    summary="Update an order item (auth required)"
)
def update_order_item(
    oid: int,
    o: schemas.OrderItemDetailUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_order_item(db, oid, o)
    if not obj:
        raise HTTPException(status_code=404, detail="Order item not found")
    return obj

@router.delete(
    "/{oid}",
    response_model=schemas.OrderItemDetailRead,
    summary="Delete an order item (auth required)"
)
def delete_order_item(
    oid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_order_item(db, oid)
    if not obj:
        raise HTTPException(status_code=404, detail="Order item not found")
    return obj
