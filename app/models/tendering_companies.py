from sqlalchemy import (
    Column, Integer, String, Text, Date, Numeric, Enum, ForeignKey, ARRAY
)
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class CurrencyEnum(str, enum.Enum):
    AED = "AED"
    EUR = "EUR"
    USD = "USD"

class PendingStatusEnum(str, enum.Enum):
    TO_BE_RELEASED = "To be released"
    IN_EFFECT     = "In effect"
    RELEASED      = "Released (By DEWA)"

class TenderingCompanies(Base):
    __tablename__ = "tendering_companies"

    tendering_companies_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    tender_no = Column(
        String(50), ForeignKey("tenders.tender_no", ondelete="CASCADE"), nullable=False, index=True, unique=True
    )
    company_id = Column(
        Integer,
        ForeignKey("company_master.company_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tender_id = Column(
        Integer, ForeignKey("tenders.tender_id", ondelete="CASCADE"), nullable=False, index=True
    )

    tender_receipt_no        = Column(String(100), nullable=True)
    tbg_no                   = Column(String(100), nullable=True)
    tbg_issuing_bank         = Column(String(100), nullable=True)
    tender_deposit_receipt_no= Column(String(100), nullable=True)
    cheque_no                = Column(String(50),  nullable=True)
    tt_ref                   = Column(String(100), nullable=True)
    tt_date                  = Column(Date, nullable=True)
    document_date            = Column(Date, nullable=True)
    tbg_value                = Column(Numeric(12,2), nullable=True)
    tbg_expiry_date          = Column(Date, nullable=True)
    tbg_submitted_date       = Column(Date, nullable=True)
    tbg_release_date_dewa    = Column(Date, nullable=True)
    tbg_release_date_bank    = Column(Date, nullable=True)
    tender_extension_dates   = Column(ARRAY(Date), nullable=True)
    tendering_currency       = Column(Enum(CurrencyEnum), nullable=False, default=CurrencyEnum.AED)
    discount_percent         = Column(Numeric(5,2), nullable=True)
    remarks                  = Column(Text, nullable=True)
    pending_status           = Column(Enum(PendingStatusEnum), nullable=False, default=PendingStatusEnum.TO_BE_RELEASED)

    # relationships
    tender   = relationship("Tender", back_populates="tendering_companies")
    company  = relationship("CompanyMaster")
    items = relationship(
        "TenderCompanyItem",
        back_populates="tendering_company",
        cascade="all, delete-orphan",
    )
    post_tender_clarifications = relationship(
        "PostTenderClarification",
        back_populates="tendering_company",
        cascade="all, delete-orphan",
        order_by="PostTenderClarification.ptc_no"
    )
    pre_tender_clarifications = relationship(
        "PreTenderClarification",
        back_populates="tendering_company",
        cascade="all, delete-orphan",
        order_by="PreTenderClarification.pre_ptc_no"
    )


    def __repr__(self) -> str:
        return (
            f"<TenderingCompanies(id={self.tendering_companies_id!r}, "
            f"tender_id={self.tender_id!r}, company_id={self.company_id!r})>"
        )
