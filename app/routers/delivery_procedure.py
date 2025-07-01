from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import app.cruds.delivery_procedure as cruds
import app.schemas.delivery_procedure as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/delivery-procedures", tags=["delivery-procedures"])

@router.get(
    "/",
    response_model=List[schemas.DeliveryProcedureRead]
)
def list_dps(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_delivery_procedures(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.DeliveryProcedureRead,
    status_code=status.HTTP_201_CREATED
)
def create_dp(
    dp: schemas.DeliveryProcedureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj, err = cruds.create_delivery_procedure(db, dp)
    if err == "lot_not_found":
        raise HTTPException(status_code=404, detail="Lot not found")
    if err == "order_item_not_found":
        raise HTTPException(status_code=404, detail="Order item not found")
    return obj

@router.get(
    "/{dp_id}",
    response_model=schemas.DeliveryProcedureRead
)
def read_dp(
    dp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_delivery_procedure(db, dp_id)
    if not obj:
        raise HTTPException(status_code=404, detail="DeliveryProcedure not found")
    return obj

@router.put(
    "/{dp_id}",
    response_model=schemas.DeliveryProcedureRead
)
def replace_dp(
    dp_id: int,
    dp: schemas.DeliveryProcedureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_delivery_procedure(db, dp_id)
    if not existing:
        raise HTTPException(status_code=404, detail="DeliveryProcedure not found")
    for k, v in dp.dict().items():
        setattr(existing, k, v)
    db.commit()
    db.refresh(existing)
    return existing

@router.patch(
    "/{dp_id}",
    response_model=schemas.DeliveryProcedureRead
)
def update_dp(
    dp_id: int,
    dp: schemas.DeliveryProcedureUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_delivery_procedure(db, dp_id, dp)
    if not obj:
        raise HTTPException(status_code=404, detail="DeliveryProcedure not found")
    return obj

@router.delete(
    "/{dp_id}",
    response_model=schemas.DeliveryProcedureRead
)
def delete_dp(
    dp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_delivery_procedure(db, dp_id)
    if not obj:
        raise HTTPException(status_code=404, detail="DeliveryProcedure not found")
    return obj
