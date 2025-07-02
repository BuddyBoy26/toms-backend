from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.cruds.tender_company_item as cruds
import app.schemas.tender_company_item as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["tender-items"])

@router.get("/", response_model=list[schemas.TenderCompanyItemRead])
def list_items(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_items(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.TenderCompanyItemRead,
    status_code=status.HTTP_201_CREATED,
)
def create_item(
    i: schemas.TenderCompanyItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj, err = cruds.create_item(db, i)
    if err == "parent_not_found":
        raise HTTPException(status_code=404, detail="Parent tendering entry not found")
    return obj

@router.get("/{iid}", response_model=schemas.TenderCompanyItemRead)
def read_item(
    iid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_item(db, iid)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    return obj

@router.put("/{iid}", response_model=schemas.TenderCompanyItemRead)
def replace_item(
    iid: int,
    i: schemas.TenderCompanyItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = cruds.get_item(db, iid)
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")
    # full replace—including re-defaulting discount if needed
    obj, err = cruds.create_item(db, i)  # simpler: delete & recreate
    if err:
        raise HTTPException(status_code=404, detail="Parent tendering entry not found")
    # delete old one
    cruds.delete_item(db, iid)
    return obj

@router.patch("/{iid}", response_model=schemas.TenderCompanyItemRead)
def update_item(
    iid: int,
    i: schemas.TenderCompanyItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_item(db, iid, i)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    return obj

@router.delete("/{iid}", response_model=schemas.TenderCompanyItemRead)
def delete_item(
    iid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_item(db, iid)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    return obj
