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

    # HEADING: Basic Information
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
    po_commencemnt_date       = Column(Date, nullable=True)

    order_value                = Column(Numeric(14, 4), nullable=False)
    currency                   = Column(Enum(CurrencyEnum), nullable=False)
    order_value_aed            = Column(Numeric(14, 4), nullable=False)
    revised_value_lme          = Column(Numeric(14, 4), nullable=True)
    revised_value_lme_aed      = Column(Numeric(14, 4), nullable=True)
    kka_commission_percent     = Column(Numeric(5,2), nullable=False, default=5.00)
    old_po_id                  = Column(
        Integer,
        ForeignKey("order_details.order_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )  #Additional order for old PO
    no_of_consignments         = Column(Integer, nullable=True)

    #HEADING: Order Conirmation
    order_confirmation_no      = Column(String(100), nullable=True)
    order_confirmation_letter_ref = Column(String(100), nullable=True)
    order_confirmation_date    = Column(Date, nullable=True)
    po_confirmation_date_srm   = Column(Date, nullable=True)

    #HEADING: Delivery Details
    last_contractual_delivery  = Column(Date, nullable=True)
    actual_last_delivery       = Column(Date, nullable=True)
    
    #HEADING: Drawing
    drawing_submission_date    = Column(Date, nullable=True)
    drawing_approval_date      = Column(Date, nullable=True)
    drawing_number             = Column(String(100), nullable=True)
    drawing_initial_version = Column(String(50), nullable=True)
    drawing_current_version  = Column(String(50), nullable=True)
    drawing_number_revised    = Column(String(100), nullable=True)

    remarks                    = Column(String(1000), nullable=True)


    company                    = relationship("CompanyMaster")
    tender                     = relationship("Tender")
    old_po                     = relationship("OrderDetail", remote_side=[order_id])
    lots = relationship("LotMonitoring", back_populates="order")
    # delivery_procedures = relationship("DeliveryProcedure", back_populates="order")
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
        order_by="OrderEvent.event_date"
    )

    drawings = relationship(
    "DrawingDetails",
    back_populates="order",
    cascade="all, delete-orphan"
)


    def __repr__(self) -> str:
        return (
            f"<OrderDetail(id={self.order_id!r}, po_number={self.po_number!r}, "
            f"company_id={self.company_id!r}, tender_id={self.tender_id!r})>"
        )
