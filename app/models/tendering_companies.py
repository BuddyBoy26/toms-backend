from sqlalchemy import (
    Column, Integer, String, Text, Date, Numeric, Enum, ForeignKey
)
from sqlalchemy.dialects.postgresql import ARRAY
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
    # Header / receipt section
    __tablename__ = "tendering_companies"

    tendering_companies_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True
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
    tender_receipt_no         = Column(String(100), nullable=True)
    debit_advice_no           = Column(String(100), nullable=True)
    debit_advice_date           = Column(Date, nullable=True)

    # "TBG details" to be dispalyed as subsection
    #Frontend will have options wether tbg or credit card through integer value managed be a radio button
    #Show if TBG is selected
    tbg_credit_card_option   = Column(Integer, nullable=False, default=0)  # 0: TBG, 1: Credit Card
    tbg_no                    = Column(String(100), nullable=True)
    tbg_issuing_bank          = Column(String(100), nullable=True)
    tender_deposit_receipt_no = Column(String(100), nullable=True)
    tendering_currency        = Column(Enum(CurrencyEnum), nullable=False, default=CurrencyEnum.AED)
    # cheque_no                 = Column(String(50),  nullable=True)
    #show if credit card is selected
    credit_card_payment_ref = Column(String(100), nullable=True)
    remarks                   = Column(Text, nullable=True)
    # credit_card_payment_date = Column(Date, nullable=True)
    # credit_card_payment_amount = Column(Numeric(14, 4), nullable=True)
    # tt_ref                    = Column(String(100), nullable=True)
    # tt_date                   = Column(Date, nullable=True)
    # document_date             = Column(Date, nullable=True)
    # continue with section
    tbg_value                 = Column(Numeric(14, 4), nullable=True)
    tbg_date                  = Column(Date, nullable=True)
    tbg_expiry_date           = Column(Date, nullable=True)
    tbg_submitted_date        = Column(Date, nullable=True)
    tbg_release_date_dewa     = Column(Date, nullable=True)
    tbg_release_date_bank     = Column(Date, nullable=True)
    dewa_enbd_ref         = Column(String(100), nullable=True)
    
    #Show a table of dates on the left with an input field and add option on the right
    tender_extension_dates    = Column(ARRAY(Date), nullable=True)
    # discount_percent          = Column(Numeric(5,2), nullable=True)
    # pending_status            = Column(Enum(PendingStatusEnum), nullable=False, default=PendingStatusEnum.TO_BE_RELEASED)

    # Section Counter Guarantee Details
    cg_bank                   = Column(String(100), nullable=True)
    cg_no                     = Column(String(100), nullable=True)
    cg_date                   = Column(Date, nullable=True)
    cg_expiry_date            = Column(Date, nullable=True)

    # Delivery Weeks
    delivery_commencement_weeks = Column(Integer, nullable=True)
    delivery_completion_weeks   = Column(Integer, nullable=True)
    

    # Just a new section with 6 radio buttons
    
    tender_bought             = Column(Integer, nullable=False, default=0)  # 0/1 boolean
    participated              = Column(Integer, nullable=False, default=0)
    result_saved              = Column(Integer, nullable=False, default=0)
    evaluations_received      = Column(Integer, nullable=False, default=0)
    memo                      = Column(Integer, nullable=False, default=0)
    po_copies                 = Column(Integer, nullable=False, default=0)

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
