from pydantic import BaseModel
from typing import List, Optional
from .product_master import ProductMasterRead  # forward import


# ----------------- Base -----------------
class CompanyMasterBase(BaseModel):
    company_name: str
    business_description: str
    country: str


# ----------------- Create -----------------
class CompanyMasterCreate(CompanyMasterBase):
    """All fields required to create."""
    # Accept product_ids when creating a company
    product_ids: Optional[List[int]] = []


# ----------------- Update -----------------
class CompanyMasterUpdate(BaseModel):
    """All fields optional for partial update."""
    company_name: Optional[str] = None
    business_description: Optional[str] = None
    country: Optional[str] = None
    # Accept product_ids when updating a company
    product_ids: Optional[List[int]] = []


# ----------------- Read -----------------
class CompanyMasterRead(CompanyMasterBase):
    company_id: int
    # Return full product details in response
    products: List[ProductMasterRead] = []

    class Config:
        from_attributes = True
