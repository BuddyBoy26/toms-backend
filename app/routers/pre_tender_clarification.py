from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import app.cruds.pre_tender_clarification as cruds
import app.schemas.pre_tender_clarification as schemas
from ..database import get_db
from .auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/pre-ptcs", tags=["pre-ptcs"])

@router.get(
    "/",
    response_model=List[schemas.PreTenderClarificationRead]
)
def list_pre_ptcs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_pre_ptcs(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.PreTenderClarificationRead,
    status_code=status.HTTP_201_CREATED
)
def create_pre_ptc(
    ptc: schemas.PreTenderClarificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj, err = cruds.create_pre_ptc(db, ptc)
    if err == "tendering_company_not_found":
        raise HTTPException(status_code=404, detail="TenderingCompanies entry not found")
    return obj

@router.get(
    "/{ptc_id}",
    response_model=schemas.PreTenderClarificationRead
)
def read_pre_ptc(
    ptc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_pre_ptc(db, ptc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="PreTenderClarification not found")
    return obj

@router.put(
    "/{ptc_id}",
    response_model=schemas.PreTenderClarificationRead
)
def replace_pre_ptc(
    ptc_id: int,
    ptc: schemas.PreTenderClarificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_pre_ptc(db, ptc_id)
    if not existing:
        raise HTTPException(status_code=404, detail="PreTenderClarification not found")
    for k, v in ptc.dict().items():
        setattr(existing, k, v)
    db.commit()
    db.refresh(existing)
    return existing

@router.patch(
    "/{ptc_id}",
    response_model=schemas.PreTenderClarificationRead
)
def update_pre_ptc(
    ptc_id: int,
    ptc: schemas.PreTenderClarificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_pre_ptc(db, ptc_id, ptc)
    if not obj:
        raise HTTPException(status_code=404, detail="PreTenderClarification not found")
    return obj

@router.delete(
    "/{ptc_id}",
    response_model=schemas.PreTenderClarificationRead
)
def delete_pre_ptc(
    ptc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_pre_ptc(db, ptc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="PreTenderClarification not found")
    return obj

@router.get(
    "/outstanding",
    response_model=List[schemas.PreTenderClarificationRead],
    summary="List PTCs past reply deadline (for reminders)"
)
def list_outstanding_pre_ptcs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.list_outstanding_pre_ptcs(db)
