from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import app.cruds.order_event as cruds
import app.schemas.order_event as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["order-events"])

@router.get(
    "/",
    response_model=List[schemas.OrderEventRead],
    summary="List all order events (chronological)"
)
def list_order_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_order_events(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.OrderEventRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order event"
)
def create_order_event(
    ev: schemas.OrderEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj, err = cruds.create_order_event(db, ev)
    if err == "order_not_found":
        raise HTTPException(status_code=404, detail="Order not found")
    return obj

@router.get(
    "/{oe_id}",
    response_model=schemas.OrderEventRead,
    summary="Get a single order event"
)
def read_order_event(
    oe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_order_event(db, oe_id)
    if not obj:
        raise HTTPException(status_code=404, detail="OrderEvent not found")
    return obj

@router.put(
    "/{oe_id}",
    response_model=schemas.OrderEventRead,
    summary="Replace an order event"
)
def replace_order_event(
    oe_id: int,
    ev: schemas.OrderEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_order_event(db, oe_id)
    if not existing:
        raise HTTPException(status_code=404, detail="OrderEvent not found")
    for k, v in ev.dict().items():
        setattr(existing, k, v)
    db.commit()
    db.refresh(existing)
    return existing

@router.patch(
    "/{oe_id}",
    response_model=schemas.OrderEventRead,
    summary="Update an order event"
)
def update_order_event(
    oe_id: int,
    ev: schemas.OrderEventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_order_event(db, oe_id, ev)
    if not obj:
        raise HTTPException(status_code=404, detail="OrderEvent not found")
    return obj

@router.delete(
    "/{oe_id}",
    response_model=schemas.OrderEventRead,
    summary="Delete an order event"
)
def delete_order_event(
    oe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_order_event(db, oe_id)
    if not obj:
        raise HTTPException(status_code=404, detail="OrderEvent not found")
    return obj
