from pydantic import BaseModel
from typing import List
from .product_master import ProductMasterRead  # forward import

class CompanyMasterBase(BaseModel):
    company_name: str
    business_description: str

class CompanyMasterCreate(CompanyMasterBase):
    """All fields required to create."""
    pass

class CompanyMasterUpdate(BaseModel):
    """All fields optional for partial update."""
    company_name: str | None = None
    business_description: str | None = None

class CompanyMasterRead(CompanyMasterBase):
    company_id: int
    products: List[ProductMasterRead] = []

    class Config:
        from_attributes = True
