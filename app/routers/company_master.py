from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.cruds.company_master as cruds
import app.schemas.company_master as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/companies", tags=["companies"])

@router.get(
    "/",
    response_model=list[schemas.CompanyMasterRead],
    summary="List companies (auth required)",
)
def list_companies(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_companies(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.CompanyMasterRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new company (auth required)",
)
def create_company(
    c: schemas.CompanyMasterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.create_company(db, c)

@router.get(
    "/{cid}",
    response_model=schemas.CompanyMasterRead,
    summary="Get a company by ID (auth required)",
)
def read_company(
    cid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_company(db, cid)
    if not obj:
        raise HTTPException(status_code=404, detail="Company not found")
    return obj

@router.put(
    "/{cid}",
    response_model=schemas.CompanyMasterRead,
    summary="Replace a company (auth required)",
)
def replace_company(
    cid: int,
    c: schemas.CompanyMasterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_company(db, cid)
    if not obj:
        raise HTTPException(status_code=404, detail="Company not found")
    # full replace
    obj.company_name = c.company_name
    obj.business_description = c.business_description
    db.commit()
    db.refresh(obj)
    return obj

@router.patch(
    "/{cid}",
    response_model=schemas.CompanyMasterRead,
    summary="Update a company (partial, auth required)",
)
def update_company(
    cid: int,
    c: schemas.CompanyMasterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_company(db, cid, c)
    if not obj:
        raise HTTPException(status_code=404, detail="Company not found")
    return obj

@router.delete(
    "/{cid}",
    response_model=schemas.CompanyMasterRead,
    summary="Delete a company (auth required)",
)
def delete_company(
    cid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_company(db, cid)
    if not obj:
        raise HTTPException(status_code=404, detail="Company not found")
    return obj
