from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.cruds.performance_guarantee as cruds
import app.schemas.performance_guarantee as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/performance-guarantees",
    tags=["performance-guarantees"]
)

@router.get(
    "/",
    response_model=list[schemas.PerformanceGuaranteeRead]
)
def list_pgs(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_performance_guarantees(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.PerformanceGuaranteeRead,
    status_code=status.HTTP_201_CREATED
)
def create_pg(
    pg: schemas.PerformanceGuaranteeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj, err = cruds.create_performance_guarantee(db, pg)
    if err == "order_not_found":
        raise HTTPException(status_code=404, detail="Order not found")
    return obj

@router.get(
    "/{pg_id}",
    response_model=schemas.PerformanceGuaranteeRead
)
def read_pg(
    pg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_performance_guarantee(db, pg_id)
    if not obj:
        raise HTTPException(status_code=404, detail="PerformanceGuarantee not found")
    return obj

@router.put(
    "/{pg_id}",
    response_model=schemas.PerformanceGuaranteeRead
)
def replace_pg(
    pg_id: int,
    pg: schemas.PerformanceGuaranteeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_performance_guarantee(db, pg_id)
    if not existing:
        raise HTTPException(status_code=404, detail="PerformanceGuarantee not found")
    for k, v in pg.dict().items():
        setattr(existing, k, v)
    db.commit()
    db.refresh(existing)
    return existing

@router.patch(
    "/{pg_id}",
    response_model=schemas.PerformanceGuaranteeRead
)
def update_pg(
    pg_id: int,
    pg: schemas.PerformanceGuaranteeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_performance_guarantee(db, pg_id, pg)
    if not obj:
        raise HTTPException(status_code=404, detail="PerformanceGuarantee not found")
    return obj

@router.delete(
    "/{pg_id}",
    response_model=schemas.PerformanceGuaranteeRead
)
def delete_pg(
    pg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_performance_guarantee(db, pg_id)
    if not obj:
        raise HTTPException(status_code=404, detail="PerformanceGuarantee not found")
    return obj
