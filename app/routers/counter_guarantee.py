from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

import app.cruds.counter_guarantee as cruds
import app.schemas.counter_guarantee as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User
from app.models.counter_guarantee import GuaranteeTypeEnum

router = APIRouter(tags=["counter-guarantees"])

# existing CRUD endpoints...

@router.get(
    "/refnumbers/",
    response_model=List[str],
    summary="List all guarantee_ref_number for a given type (for dropdown)"
)
def get_ref_numbers(
    guarantee_type: GuaranteeTypeEnum = Query(..., description="TBG, PBG or MPG"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    refs = cruds.list_ref_numbers_by_type(db, guarantee_type)
    return refs

# CRUD endpoints follow
@router.get("/", response_model=list[schemas.CounterGuaranteeRead])
def list_cgs(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_counter_guarantees(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.CounterGuaranteeRead,
    status_code=status.HTTP_201_CREATED,
)
def create_cg(
    cg: schemas.CounterGuaranteeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.create_counter_guarantee(db, cg)

@router.get("/{cg_id}", response_model=schemas.CounterGuaranteeRead)
def read_cg(
    cg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_counter_guarantee(db, cg_id)
    if not obj:
        raise HTTPException(status_code=404, detail="CounterGuarantee not found")
    return obj

@router.put("/{cg_id}", response_model=schemas.CounterGuaranteeRead)
def replace_cg(
    cg_id: int,
    cg: schemas.CounterGuaranteeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_counter_guarantee(db, cg_id)
    if not existing:
        raise HTTPException(status_code=404, detail="CounterGuarantee not found")
    for k, v in cg.dict().items():
        setattr(existing, k, v)
    db.commit()
    db.refresh(existing)
    return existing

@router.patch("/{cg_id}", response_model=schemas.CounterGuaranteeRead)
def update_cg(
    cg_id: int,
    cg: schemas.CounterGuaranteeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_counter_guarantee(db, cg_id, cg)
    if not obj:
        raise HTTPException(status_code=404, detail="CounterGuarantee not found")
    return obj

@router.delete("/{cg_id}", response_model=schemas.CounterGuaranteeRead)
def delete_cg(
    cg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_counter_guarantee(db, cg_id)
    if not obj:
        raise HTTPException(status_code=404, detail="CounterGuarantee not found")
    return obj
