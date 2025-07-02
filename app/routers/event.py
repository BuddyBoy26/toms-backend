from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import app.cruds.event as cruds
import app.schemas.event as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["events"])

@router.get("/", response_model=List[schemas.EventRead])
def list_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List events in chronological order.
    Frontend calendar can consume this and render.
    """
    return cruds.get_events(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.EventRead,
    status_code=status.HTTP_201_CREATED
)
def create_event(
    e: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.create_event(db, e)

@router.get("/{eid}", response_model=schemas.EventRead)
def read_event(
    eid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_event(db, eid)
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")
    return obj

@router.put("/{eid}", response_model=schemas.EventRead)
def replace_event(
    eid: int,
    e: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_event(db, eid)
    if not existing:
        raise HTTPException(status_code=404, detail="Event not found")
    # full replace
    for k, v in e.dict().items():
        setattr(existing, k, v)
    db.commit()
    db.refresh(existing)
    return existing

@router.patch("/{eid}", response_model=schemas.EventRead)
def update_event(
    eid: int,
    e: schemas.EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_event(db, eid, e)
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")
    return obj

@router.delete("/{eid}", response_model=schemas.EventRead)
def delete_event(
    eid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_event(db, eid)
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")
    return obj
