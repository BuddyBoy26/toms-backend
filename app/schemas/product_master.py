from pydantic import BaseModel

class ProductMasterBase(BaseModel):
    product_name: str

class ProductMasterCreate(ProductMasterBase):
    pass

class ProductMasterUpdate(BaseModel):
    product_name: str | None = None

class ProductMasterRead(BaseModel):
    product_id: int
    product_name: str

    class Config:
        from_attributes = True
