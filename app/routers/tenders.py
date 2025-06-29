from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.cruds as cruds, app.schemas as schemas
from app.models import User

from ..routers.auth import get_current_user

from ..database import get_db

router = APIRouter()

@router.get("/tenders", response_model=list[schemas.TenderRead])
def list_tenders(skip: int=0, limit: int=50, db: Session=Depends(get_db)):
    return cruds.get_tenders(db, skip, limit)

@router.post("/tenders", response_model=schemas.TenderRead, status_code=status.HTTP_201_CREATED)
def create_tender(t: schemas.TenderCreate, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return cruds.create_tender(db, t, current_user.id)

@router.get("/tenders/{tid}", response_model=schemas.TenderRead)
def read_tender(tid: int, db: Session=Depends(get_db)):
    obj = cruds.get_tender(db, tid)
    if not obj: raise HTTPException(404, "Tender not found")
    return obj

@router.put("/tenders/{tid}", response_model=schemas.TenderRead)
def update_tender(tid: int, t: schemas.TenderBase, db: Session=Depends(get_db)):
    obj = cruds.update_tender(db, tid, t)
    if not obj: raise HTTPException(404, "Tender not found")
    return obj

@router.delete("/tenders/{tid}", response_model=schemas.TenderRead)
def delete_tender(tid: int, db: Session=Depends(get_db)):
    obj = cruds.delete_tender(db, tid)
    if not obj: raise HTTPException(404, "Tender not found")
    return obj
