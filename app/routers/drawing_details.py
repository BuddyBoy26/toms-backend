from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from app.schemas.drawing_details import (
    DrawingDetailsCreate,
    DrawingDetailsRead,
)
import app.cruds.drawing_details as cruds

router = APIRouter(tags=["drawing-details"])

@router.post(
    "/",
    response_model=DrawingDetailsRead,
    status_code=status.HTTP_201_CREATED,
)
def create_dd(
    dd_in: DrawingDetailsCreate,
    db: Session = Depends(get_db),
):
    return cruds.create_drawing_details(db=db, dd_in=dd_in)

@router.get(
    "/",
    response_model=List[DrawingDetailsRead],
)
def read_all_dd(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return cruds.list_drawing_details(db=db, skip=skip, limit=limit)

@router.get(
    "/{dd_id}",
    response_model=DrawingDetailsRead,
)
def read_dd(
    dd_id: int,
    db: Session = Depends(get_db),
):
    dd = cruds.get_drawing_details(db=db, dd_id=dd_id)
    if not dd:
        raise HTTPException(status_code=404, detail="Not found")
    return dd

@router.put(
    "/{dd_id}",
    response_model=DrawingDetailsRead,
)
def update_dd(
    dd_id: int,
    dd_in: DrawingDetailsCreate,
    db: Session = Depends(get_db),
):
    return cruds.update_drawing_details(db=db, dd_id=dd_id, dd_in=dd_in)

@router.delete(
    "/{dd_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_dd(
    dd_id: int,
    db: Session = Depends(get_db),
):
    cruds.delete_drawing_details(db=db, dd_id=dd_id)
