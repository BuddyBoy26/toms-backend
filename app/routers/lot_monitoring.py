from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import app.cruds.lot_monitoring as cruds
import app.schemas.lot_monitoring as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/lots", tags=["lots"])

@router.get("/", response_model=List[schemas.LotMonitoringRead])
def list_lots(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_lots(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.LotMonitoringRead,
    status_code=status.HTTP_201_CREATED
)
def create_lot(
    lot: schemas.LotMonitoringCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj, err = cruds.create_lot(db, lot)
    if err == "order_item_not_found":
        raise HTTPException(status_code=404, detail="Order item not found")
    return obj

@router.get("/{lot_id}", response_model=schemas.LotMonitoringRead)
def read_lot(
    lot_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_lot(db, lot_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Lot not found")
    return obj

@router.put("/{lot_id}", response_model=schemas.LotMonitoringRead)
def replace_lot(
    lot_id: str,
    lot: schemas.LotMonitoringCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_lot(db, lot_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Lot not found")
    for k,v in lot.dict().items():
        setattr(existing, k, v)
    db.commit()
    db.refresh(existing)
    return existing

@router.patch("/{lot_id}", response_model=schemas.LotMonitoringRead)
def update_lot(
    lot_id: str,
    lot: schemas.LotMonitoringUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_lot(db, lot_id, lot)
    if not obj:
        raise HTTPException(status_code=404, detail="Lot not found")
    return obj

@router.delete("/{lot_id}", response_model=schemas.LotMonitoringRead)
def delete_lot(
    lot_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_lot(db, lot_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Lot not found")
    return obj
