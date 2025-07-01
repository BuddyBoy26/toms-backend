from sqlalchemy import (
    Column, Integer, String, Date,
    ForeignKey, UniqueConstraint, ForeignKeyConstraint
)
from sqlalchemy.orm import relationship
from ..database import Base

class PostTenderClarification(Base):
    __tablename__ = "post_tender_clarifications"
    __table_args__ = (
        # preserve your existing unique constraint
        UniqueConstraint("tender_id", "company_id", "ptc_no", name="uq_ptc"),
        # add a composite foreign key to tendering_companies
        ForeignKeyConstraint(
            ["tender_id", "company_id"],
            ["tendering_companies.tender_id", "tendering_companies.company_id"],
            name="fk_ptc_to_tendering_companies",
            ondelete="CASCADE"
        ),
    )

    ptc_id                    = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tender_id                 = Column(Integer, nullable=False, index=True)
    company_id                = Column(Integer, nullable=False, index=True)
    ptc_no                    = Column(Integer, nullable=False)
    ptc_ref_no                = Column(String(100), nullable=False)
    ptc_date                  = Column(Date, nullable=False)
    ptc_received_date         = Column(Date, nullable=False)
    ptc_reply_required_by     = Column(Date, nullable=False)
    ptc_reply_submission_date = Column(Date, nullable=True)

    # keep your existing relationships
    tender                    = relationship("Tender", back_populates="post_tender_clarifications")
    company                   = relationship("CompanyMaster", back_populates="post_tender_clarifications")
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
