from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base, relationship

class ProductMaster(Base):
    __tablename__ = "product_master"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), nullable=False, index=True)

    company_id = Column(
        Integer,
        ForeignKey("company_master.company_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    company = relationship("CompanyMaster", back_populates="products")

    def __repr__(self) -> str:
        return (
            f"<ProductMaster("
            f"product_id={self.product_id!r}, "
            f"product_name={self.product_name!r})>"
        )
