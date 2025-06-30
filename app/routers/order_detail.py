from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.cruds.order_detail as cruds
import app.schemas.order_detail as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User
from app.cruds.company_master import get_company
from app.cruds.tender import get_tender

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=list[schemas.OrderDetailRead])
def list_orders(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_orders(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.OrderDetailRead,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    o: schemas.OrderDetailCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ensure FK integrity
    if not get_company(db, o.company_id):
        raise HTTPException(404, "Company not found")
    if not get_tender(db, o.tender_id):
        raise HTTPException(404, "Tender not found")
    return cruds.create_order(db, o)

@router.get("/{oid}", response_model=schemas.OrderDetailRead)
def read_order(
    oid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_order(db, oid)
    if not obj:
        raise HTTPException(404, "Order not found")
    return obj

@router.put("/{oid}", response_model=schemas.OrderDetailRead)
def replace_order(
    oid: int,
    o: schemas.OrderDetailCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_order(db, oid)
    if not obj:
        raise HTTPException(404, "Order not found")
    # full replace
    for k, v in o.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.patch("/{oid}", response_model=schemas.OrderDetailRead)
def update_order(
    oid: int,
    o: schemas.OrderDetailUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_order(db, oid, o)
    if not obj:
        raise HTTPException(404, "Order not found")
    return obj

@router.delete("/{oid}", response_model=schemas.OrderDetailRead)
def delete_order(
    oid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_order(db, oid)
    if not obj:
        raise HTTPException(404, "Order not found")
    return obj
