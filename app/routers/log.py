from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import cruds, schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User  # your User ORM

router = APIRouter(prefix="/logs", tags=["logs"])

@router.post(
    "/",
    response_model=schemas.log.LogRead,
    status_code=status.HTTP_201_CREATED,
)
def create_log(
    log_in: schemas.log.LogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.log.create_log(db=db, log_in=log_in, user_id=current_user.id)

@router.get(
    "/",
    response_model=List[schemas.log.LogRead],
)
def read_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return cruds.log.get_logs(db=db, skip=skip, limit=limit)

@router.get(
    "/{log_id}",
    response_model=schemas.log.LogRead,
)
def read_log(
    log_id: int,
    db: Session = Depends(get_db),
):
    db_log = cruds.log.get_log(db=db, log_id=log_id)
    if not db_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Log with id={log_id} not found",
        )
    return db_log
