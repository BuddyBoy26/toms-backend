from sqlalchemy import (
    Column, Integer, String, Date,
    ForeignKey, UniqueConstraint, ForeignKeyConstraint
)
from sqlalchemy.orm import relationship
from ..database import Base

class PostTenderClarification(Base):
    __tablename__ = "post_tender_clarifications"

    ptc_id                    = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tc_id     = Column(
        "tendering_companies_id",
        Integer,
        ForeignKey("tendering_companies.tendering_companies_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ptc_no                    = Column(Integer, nullable=False)
    ptc_ref_no                = Column(String(100), nullable=False)
    ptc_date                  = Column(Date, nullable=False)
    ptc_received_date         = Column(Date, nullable=False)
    ptc_reply_required_by     = Column(Date, nullable=False)
    ptc_reply_submission_date = Column(Date, nullable=True)

    # keep your existing relationships
    # tender                    = relationship("Tender", back_populates="post_tender_clarifications")
    # company                   = relationship("CompanyMaster", back_populates="post_tender_clarifications")
    # new relationship into the join‐table
    tendering_company         = relationship(
        "TenderingCompanies",
        back_populates="post_tender_clarifications",
        uselist=False,
    )

    def __repr__(self) -> str:
        return (
            f"<PostTenderClarification(ptc_id={self.ptc_id!r}, "
            f"tender_id={self.tender_id!r}, company_id={self.company_id!r}, ptc_no={self.ptc_no!r})>"
        )
