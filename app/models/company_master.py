from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..database import Base

class CompanyMaster(Base):
    __tablename__ = "company_master"

    company_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    business_description = Column(Text, nullable=False)

    products = relationship(
    "ProductMaster",
    back_populates="company",
    cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<CompanyMaster("
            f"company_id={self.company_id!r}, "
            f"company_name={self.company_name!r}, "
            f"business_description={self.business_description!r})>"
        )
