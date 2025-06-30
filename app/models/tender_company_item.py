from sqlalchemy import (
    Column, Integer, String, Numeric, ForeignKey
)
from sqlalchemy.orm import relationship
from ..database import Base

class TenderCompanyItem(Base):
    __tablename__ = "tender_company_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tendering_companies_id = Column(
        Integer,
        ForeignKey("tendering_companies.tendering_companies_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    item_no_dewa      = Column(String(100), nullable=False, index=True)
    discount_percent  = Column(Numeric(5,2), nullable=False)

    tendering_company = relationship(
        "TenderingCompanies",
        back_populates="items",
    )

    def __repr__(self) -> str:
        return (
            f"<TenderCompanyItem("
            f"id={self.id!r}, "
            f"tendering_companies_id={self.tendering_companies_id!r}, "
            f"item_no_dewa={self.item_no_dewa!r}, "
            f"discount_percent={self.discount_percent!r})>"
        )
