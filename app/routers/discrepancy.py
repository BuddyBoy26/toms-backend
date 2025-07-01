from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import app.cruds.discrepancy as cruds
import app.schemas.discrepancy as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/discrepancies", tags=["discrepancies"])

@router.get("/", response_model=List[schemas.DiscrepancyRead])
def list_discrepancies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_discrepancies(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.DiscrepancyRead,
    status_code=status.HTTP_201_CREATED,
)
def create_discrepancy(
    d: schemas.DiscrepancyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj, err = cruds.create_discrepancy(db, d)
    if err == "lot_not_found":
        raise HTTPException(status_code=404, detail="Lot not found")
    return obj

@router.get("/{did}", response_model=schemas.DiscrepancyRead)
def read_discrepancy(
    did: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_discrepancy(db, did)
    if not obj:
        raise HTTPException(status_code=404, detail="Discrepancy not found")
    return obj

@router.put("/{did}", response_model=schemas.DiscrepancyRead)
def replace_discrepancy(
    did: int,
    d: schemas.DiscrepancyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_discrepancy(db, did)
    if not existing:
        raise HTTPException(status_code=404, detail="Discrepancy not found")
    for k, v in d.dict().items():
        setattr(existing, k, v)
    db.commit()
    db.refresh(existing)
    return existing

@router.patch("/{did}", response_model=schemas.DiscrepancyRead)
def update_discrepancy(
    did: int,
    d: schemas.DiscrepancyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_discrepancy(db, did, d)
    if not obj:
        raise HTTPException(status_code=404, detail="Discrepancy not found")
    return obj

@router.delete("/{did}", response_model=schemas.DiscrepancyRead)
def delete_discrepancy(
    did: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_discrepancy(db, did)
    if not obj:
        raise HTTPException(status_code=404, detail="Discrepancy not found")
    return obj
