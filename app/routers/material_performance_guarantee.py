from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.cruds.material_performance_guarantee as cruds
import app.schemas.material_performance_guarantee as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/material-performance-guarantees",
    tags=["material-performance-guarantees"]
)

@router.get("/", response_model=list[schemas.MaterialPerformanceGuaranteeRead])
def list_mpgs(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_mpgs(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.MaterialPerformanceGuaranteeRead,
    status_code=status.HTTP_201_CREATED
)
def create_mpg(
    mpg: schemas.MaterialPerformanceGuaranteeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj, err = cruds.create_mpg(db, mpg)
    if err == "order_not_found":
        raise HTTPException(status_code=404, detail="Order not found")
    return obj

@router.get("/{mpg_id}", response_model=schemas.MaterialPerformanceGuaranteeRead])
def read_mpg(
    mpg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_mpg(db, mpg_id)
    if not obj:
        raise HTTPException(status_code=404, detail="MPG not found")
    return obj

@router.put("/{mpg_id}", response_model=schemas.MaterialPerformanceGuaranteeRead])
def replace_mpg(
    mpg_id: int,
    mpg: schemas.MaterialPerformanceGuaranteeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_mpg(db, mpg_id)
    if not existing:
        raise HTTPException(status_code=404, detail="MPG not found")
    for k, v in mpg.dict().items():
        setattr(existing, k, v)
    db.commit()
    db.refresh(existing)
    return existing

@router.patch("/{mpg_id}", response_model=schemas.MaterialPerformanceGuaranteeRead])
def update_mpg(
    mpg_id: int,
    mpg: schemas.MaterialPerformanceGuaranteeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_mpg(db, mpg_id, mpg)
    if not obj:
        raise HTTPException(status_code=404, detail="MPG not found")
    return obj

@router.delete("/{mpg_id}", response_model=schemas.MaterialPerformanceGuaranteeRead])
def delete_mpg(
    mpg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_mpg(db, mpg_id)
    if not obj:
        raise HTTPException(status_code=404, detail="MPG not found")
    return obj
