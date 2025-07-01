from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import app.cruds.liquidated_damages as cruds
import app.schemas.liquidated_damages as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/liquidated-damages", tags=["liquidated-damages"])

@router.get("/", response_model=List[schemas.LiquidatedDamagesRead])
def list_lds(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_lds(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.LiquidatedDamagesRead,
    status_code=status.HTTP_201_CREATED,
)
def create_ld(
    ld: schemas.LiquidatedDamagesCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj, err = cruds.create_ld(db, ld)
    if err == "lot_not_found":
        raise HTTPException(status_code=404, detail="Lot not found")
    return obj

@router.get("/{ld_id}", response_model=schemas.LiquidatedDamagesRead)
def read_ld(
    ld_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_ld(db, ld_id)
    if not obj:
        raise HTTPException(status_code=404, detail="LiquidatedDamages not found")
    return obj

@router.put("/{ld_id}", response_model=schemas.LiquidatedDamagesRead)
def replace_ld(
    ld_id: int,
    ld: schemas.LiquidatedDamagesCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_ld(db, ld_id)
    if not existing:
        raise HTTPException(status_code=404, detail="LiquidatedDamages not found")
    for k, v in ld.dict().items():
        setattr(existing, k, v)
    db.commit()
    db.refresh(existing)
    return existing

@router.patch("/{ld_id}", response_model=schemas.LiquidatedDamagesRead)
def update_ld(
    ld_id: int,
    ld: schemas.LiquidatedDamagesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_ld(db, ld_id, ld)
    if not obj:
        raise HTTPException(status_code=404, detail="LiquidatedDamages not found")
    return obj

@router.delete("/{ld_id}", response_model=schemas.LiquidatedDamagesRead)
def delete_ld(
    ld_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_ld(db, ld_id)
    if not obj:
        raise HTTPException(status_code=404, detail="LiquidatedDamages not found")
    return obj
