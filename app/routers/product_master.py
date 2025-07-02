from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.cruds.product_master as cruds
import app.schemas.product_master as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["products"])

@router.get("/", response_model=list[schemas.ProductMasterRead])
def list_products(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_products(db, skip, limit)

@router.post(
    "/",
    response_model=schemas.ProductMasterRead,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    p: schemas.ProductMasterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ensure the referenced company exists?
    from app.cruds.company_master import get_company
    if not get_company(db, p.company_id):
        raise HTTPException(404, "Company not found")
    return cruds.create_product(db, p)

@router.get("/{pid}", response_model=schemas.ProductMasterRead)
def read_product(
    pid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_product(db, pid)
    if not obj:
        raise HTTPException(404, "Product not found")
    return obj

@router.put("/{pid}", response_model=schemas.ProductMasterRead)
def replace_product(
    pid: int,
    p: schemas.ProductMasterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.get_product(db, pid)
    if not obj:
        raise HTTPException(404, "Product not found")
    # full replace
    obj.product_name = p.product_name
    obj.company_id = p.company_id
    db.commit()
    db.refresh(obj)
    return obj

@router.patch("/{pid}", response_model=schemas.ProductMasterRead)
def update_product(
    pid: int,
    p: schemas.ProductMasterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.update_product(db, pid, p)
    if not obj:
        raise HTTPException(404, "Product not found")
    return obj

@router.delete("/{pid}", response_model=schemas.ProductMasterRead)
def delete_product(
    pid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_product(db, pid)
    if not obj:
        raise HTTPException(404, "Product not found")
    return obj
