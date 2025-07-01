from sqlalchemy import (
    Column, Integer, String, Date, Numeric, Enum, ForeignKey
)
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class CurrencyEnum(str, enum.Enum):
    AED  = "AED"
    EUR  = "EUR"
    USD  = "USD"

class OrderDetail(Base):
    __tablename__ = "order_details"

    order_id                   = Column(Integer, primary_key=True, index=True, autoincrement=True)
    company_id                 = Column(
        Integer,
        ForeignKey("company_master.company_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    tender_id                  = Column(
        Integer,
        ForeignKey("tenders.tender_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    po_number                  = Column(String(100), nullable=False, unique=True, index=True)
    order_description          = Column(String(500), nullable=False)
    order_date                 = Column(Date, nullable=False)
    order_value                = Column(Numeric(14,2), nullable=False)
    currency                   = Column(Enum(CurrencyEnum), nullable=False)
    order_value_aed            = Column(Numeric(14,2), nullable=False)
    revised_value_lme          = Column(Numeric(14,2), nullable=True)
    revised_value_lme_aed      = Column(Numeric(14,2), nullable=True)
    order_confirmation_no      = Column(String(100), nullable=True)
    order_confirmation_date    = Column(Date, nullable=True)
    po_confirmation_date_srm   = Column(Date, nullable=True)
    drawing_submission_date    = Column(Date, nullable=True)
    drawing_approval_date      = Column(Date, nullable=True)
    last_contractual_delivery  = Column(Date, nullable=True)
    actual_last_delivery       = Column(Date, nullable=True)
    old_po_id                  = Column(
        Integer,
        ForeignKey("order_details.order_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    kka_commission_percent     = Column(Numeric(5,2), nullable=False, default=5.00)
    no_of_consignments         = Column(Integer, nullable=True)

    company                    = relationship("CompanyMaster")
    tender                     = relationship("Tender")
    old_po                     = relationship("OrderDetail", remote_side=[order_id])
    items = relationship(
        "OrderItemDetail",
        back_populates="order",
        cascade="all, delete-orphan",
    )
    performance_guarantees = relationship(
        "PerformanceGuarantee",
        back_populates="order",
        cascade="all, delete-orphan",
    )
    material_performance_guarantees = relationship(
        "MaterialPerformanceGuarantee",
        back_populates="order",
        cascade="all, delete-orphan",
    )
    events = relationship(
        "OrderEvent",
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="OrderEvent.date"
    )

    def __repr__(self) -> str:
        return (
            f"<OrderDetail(id={self.order_id!r}, po_number={self.po_number!r}, "
            f"company_id={self.company_id!r}, tender_id={self.tender_id!r})>"
        )
