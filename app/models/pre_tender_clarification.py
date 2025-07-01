from sqlalchemy import (
    Column, Integer, String, Date,
    ForeignKey, UniqueConstraint,
    ForeignKeyConstraint
)
from sqlalchemy.orm import relationship
from ..database import Base

class PreTenderClarification(Base):
    __tablename__ = "pre_tender_clarifications"

    pre_ptc_id                   = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tc_id     = Column(
        "tendering_companies_id",
        Integer,
        ForeignKey("tendering_companies.tendering_companies_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    pre_ptc_no                   = Column(Integer, nullable=False)
    pre_ptc_ref_no               = Column(String(100), nullable=False)
    pre_ptc_date                 = Column(Date, nullable=False)
    pre_ptc_received_date        = Column(Date, nullable=False)
    pre_ptc_reply_required_by    = Column(Date, nullable=False)
    pre_ptc_reply_submission_date= Column(Date, nullable=True)

    tendering_company            = relationship(
        "TenderingCompanies",
        back_populates="pre_tender_clarifications",
        uselist=False,
    )

    def __repr__(self) -> str:
        return (
            f"<PreTenderClarification(id={self.pre_ptc_id!r}, "
            f"tender_id={self.tender_id!r}, company_id={self.company_id!r}, "
            f"no={self.pre_ptc_no!r})>"
        )
