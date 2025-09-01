from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base
from .associations import company_product


class ProductMaster(Base):
    __tablename__ = "product_master"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String(255), nullable=False, index=True)

    # Many-to-many: products <-> companies
    companies = relationship(
        "CompanyMaster",
        secondary=company_product,
        back_populates="products"
    )

    items = relationship( "ItemMaster", back_populates="product", cascade="all, delete-orphan", )

    def __repr__(self) -> str:
        return (
            f"<ProductMaster("
            f"product_id={self.product_id!r}, "
            f"product_name={self.product_name!r})>"
        )
