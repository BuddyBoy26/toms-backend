from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import app.cruds.post_tender_clarification as cruds
import app.schemas.post_tender_clarification as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/ptcs", tags=["ptcs"])

@router.get("/", response_model=List[schemas.PostTenderClarificationRead])
def list_ptcs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_ptcs(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.PostTenderClarificationRead,
    status_code=status.HTTP_201_CREATED
)
def create_ptc(
    ptc: schemas.PostTenderClarificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj, err = cruds.create_ptc(db, ptc)
    if err == "tender_not_found":
        raise HTTPException(status_code=404, detail="Tender not found")
    if err == "company_not_found":
        raise HTTPException(status_code=404, detail="Company not found")
    return obj

@router.get("/{ptc_id}", response_model=schemas.PostTenderClarificationRead)
def read_ptc(
    ptc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_ptc(db, ptc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="PTC not found")
    return obj

@router.put("/{ptc_id}", response_model=schemas.PostTenderClarificationRead)
def replace_ptc(
    ptc_id: int,
    ptc: schemas.PostTenderClarificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_ptc(db, ptc_id)
    if not existing:
        raise HTTPException(status_code=404, detail="PTC not found")
    for k, v in ptc.dict().items():
        setattr(existing, k, v)
    db.commit()
    db.refresh(existing)
    return existing

@router.patch("/{ptc_id}", response_model=schemas.PostTenderClarificationRead)
def update_ptc(
    ptc_id: int,
    ptc: schemas.PostTenderClarificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_ptc(db, ptc_id, ptc)
    if not obj:
        raise HTTPException(status_code=404, detail="PTC not found")
    return obj

@router.delete("/{ptc_id}", response_model=schemas.PostTenderClarificationRead)
def delete_ptc(
    ptc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_ptc(db, ptc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="PTC not found")
    return obj

@router.get(
    "/outstanding",
    response_model=List[schemas.PostTenderClarificationRead],
    summary="List PTCs past reply deadline (for reminders)"
)
def list_outstanding(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.list_outstanding_ptcs(db)
