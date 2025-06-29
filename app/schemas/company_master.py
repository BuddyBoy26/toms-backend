from pydantic import BaseModel

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

    class Config:
        from_attributes = True
