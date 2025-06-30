from pydantic import BaseModel

class ItemMasterBase(BaseModel):
    product_id: int
    item_description: str
    hs_code: str

class ItemMasterCreate(ItemMasterBase):
    """All fields required to create an item."""
    pass

class ItemMasterUpdate(BaseModel):
    """Fields optional for partial update."""
    product_id: int | None = None
    item_description: str | None = None
    hs_code: str | None = None

class ItemMasterRead(ItemMasterBase):
    item_id: int

    class Config:
        from_attributes = True
