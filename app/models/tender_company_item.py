from sqlalchemy import Column, Integer, Numeric, ForeignKey, String, UniqueConstraint
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

    # Correct: integer FK → item_master.item_id
    item_id = Column(
        Integer,
        ForeignKey("item_master.item_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        doc="FK to item_master.item_id",
    )

    # DEWA-facing item reference (free text)
    item_no_dewa = Column(
        String(200),
        nullable=False,
        index=True,
        doc="External DEWA item reference / line description",
    )

    discount_percent = Column(Numeric(5, 2), nullable=False)
    item_price       = Column(Numeric(12, 2), nullable=False)

    # relationships
    tendering_company = relationship(
        "TenderingCompanies",
        back_populates="items",
    )

    # link to item_master table (assuming you have a mapped ItemMaster class)
    item = relationship(
        "ItemMaster",
        back_populates="tender_company_items",
        lazy="joined",
    )

    __table_args__ = (
        UniqueConstraint(
            "tendering_companies_id", "item_id", name="uq_tc_item_per_tc"
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<TenderCompanyItem("
            f"id={self.id!r}, "
            f"tendering_companies_id={self.tendering_companies_id!r}, "
            f"item_id={self.item_id!r}, "
            f"item_no_dewa={self.item_no_dewa!r}, "
            f"discount_percent={self.discount_percent!r}, "
            f"item_price={self.item_price!r}"
            f")>"
        )
