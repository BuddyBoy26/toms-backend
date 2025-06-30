from sqlalchemy import Column, String, Text, Date, Numeric, Integer
from sqlalchemy.orm import relationship
from ..database import Base

class Tender(Base):
    __tablename__ = "tenders"

    tender_id           = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tender_no           = Column(String(50), index=True, unique=True, nullable=False)
    tender_description  = Column(Text, nullable=False)
    tender_date         = Column(Date, nullable=False)
    closing_date        = Column(Date, nullable=True)
    tender_fees         = Column(Numeric(12,2), nullable=True)
    bond_guarantee_amt  = Column(Numeric(12,2), nullable=True)

    tendering_companies = relationship(
        "TenderingCompanies",
        back_populates="tender",
        cascade="all, delete-orphan",
    )

    orders = relationship(
        "OrderDetail",
        back_populates="tender",
        cascade="all, delete-orphan"
    )


    def __repr__(self) -> str:
        return (
            f"<Tender(tender_no={self.tender_no!r}, "
            f"tender_description={self.tender_description!r}, "
            f"tender_date={self.tender_date!r}, "
            f"closing_date={self.closing_date!r}, "
            f"tender_fees={self.tender_fees!r}, "
            f"bond_guarantee_amt={self.bond_guarantee_amt!r})>"
        )
