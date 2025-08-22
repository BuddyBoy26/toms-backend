from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..database import Base
from .associations import company_product


class CompanyMaster(Base):
    __tablename__ = "company_master"

    company_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    business_description = Column(Text, nullable=False)
    country = Column(String(100), nullable=False)

    # Many-to-many: companies <-> products
    products = relationship(
        "ProductMaster",
        secondary=company_product,
        back_populates="companies"
    )

    orders = relationship(
        "OrderDetail",
        back_populates="company",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<CompanyMaster("
            f"company_id={self.company_id!r}, "
            f"company_name={self.company_name!r}, "
            f"business_description={self.business_description!r}, "
            f"country={self.country!r})>"
        )
    
