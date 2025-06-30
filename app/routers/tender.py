from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.cruds.tender as cruds
import app.schemas.tender as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tenders", tags=["tenders"])

@router.get("/", response_model=list[schemas.TenderRead])
def list_tenders(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_tenders(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.TenderRead,
    status_code=status.HTTP_201_CREATED,
)
def create_tender(
    t: schemas.TenderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if cruds.get_tender(db, t.tender_no):
        raise HTTPException(status_code=400, detail="Tender number already exists")
    return cruds.create_tender(db, t)

@router.get("/{tno}", response_model=schemas.TenderRead)
def read_tender(
    tno: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_tender(db, tno)
    if not obj:
        raise HTTPException(status_code=404, detail="Tender not found")
    return obj

@router.put("/{tno}", response_model=schemas.TenderRead)
def replace_tender(
    tno: str,
    t: schemas.TenderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_tender(db, tno)
    if not obj:
        raise HTTPException(status_code=404, detail="Tender not found")
    # full replace
    for field, val in t.dict().items():
        setattr(obj, field, val)
    db.commit()
    db.refresh(obj)
    return obj

@router.patch("/{tno}", response_model=schemas.TenderRead)
def update_tender(
    tno: str,
    t: schemas.TenderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_tender(db, tno, t)
    if not obj:
        raise HTTPException(status_code=404, detail="Tender not found")
    return obj

@router.delete("/{tno}", response_model=schemas.TenderRead)
def delete_tender(
    tno: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_tender(db, tno)
    if not obj:
        raise HTTPException(status_code=404, detail="Tender not found")
    return obj
