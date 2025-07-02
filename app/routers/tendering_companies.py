from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.cruds.tendering_companies as cruds
import app.schemas.tendering_companies as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User
from app.cruds.tender import get_tender
from app.cruds.company_master import get_company

router = APIRouter(tags=["tendering"])

@router.get(
    "/",
    response_model=list[schemas.TenderingCompaniesRead],
    summary="List tendering entries (auth required)",
)
def list_tendering(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_tendering_entries(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.TenderingCompaniesRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create tendering entry (auth required)",
)
def create_tendering(
    tc: schemas.TenderingCompaniesCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ensure FK exists
    if not get_tender(db, tc.tender_id):
        raise HTTPException(status_code=404, detail="Tender not found")
    if not get_company(db, tc.company_id):
        raise HTTPException(status_code=404, detail="Company not found")
    return cruds.create_tendering_entry(db, tc)

@router.get(
    "/{tc_id}",
    response_model=schemas.TenderingCompaniesRead,
    summary="Get tendering entry (auth required)",
)
def read_tendering(
    tc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_tendering_entry(db, tc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Entry not found")
    return obj

@router.put(
    "/{tc_id}",
    response_model=schemas.TenderingCompaniesRead,
    summary="Replace tendering entry (auth required)",
)
def replace_tendering(
    tc_id: int,
    tc: schemas.TenderingCompaniesCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_tendering_entry(db, tc_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Entry not found")
    # full replace
    for k, v in tc.dict().items():
        setattr(existing, k, v)
    db.commit()
    db.refresh(existing)
    return existing

@router.patch(
    "/{tc_id}",
    response_model=schemas.TenderingCompaniesRead,
    summary="Update tendering entry (auth required)",
)
def update_tendering(
    tc_id: int,
    tc: schemas.TenderingCompaniesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_tendering_entry(db, tc_id, tc)
    if not obj:
        raise HTTPException(status_code=404, detail="Entry not found")
    return obj

@router.delete(
    "/{tc_id}",
    response_model=schemas.TenderingCompaniesRead,
    summary="Delete tendering entry (auth required)",
)
def delete_tendering(
    tc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_tendering_entry(db, tc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Entry not found")
    return obj
