from pydantic import BaseModel

class ProductMasterBase(BaseModel):
    product_name: str
    company_id: int

class ProductMasterCreate(ProductMasterBase):
    pass

class ProductMasterUpdate(BaseModel):
    product_name: str | None = None
    company_id: int | None = None

class ProductMasterRead(BaseModel):
    product_id: int
    product_name: str
    company_id: int

    class Config:
        from_attributes = True
