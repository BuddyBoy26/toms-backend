import enum
from sqlalchemy import (
    Column, Integer, String, Date,
    ForeignKey, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from ..database import Base

class DocReceiveStatusEnum(str, enum.Enum):
    ALL_RECEIVED     = "All documents received"
    PARTIAL_RECEIVED = "Partial documents received"

class DeliveryProcedure(Base):
    __tablename__ = "delivery_procedures"

    dp_id                         = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lot_id                        = Column(
        String(20),
        ForeignKey("lot_monitoring.lot_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    order_item_detail_id          = Column(
        Integer,
        ForeignKey("order_item_details.order_item_detail_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    shipment_etd                  = Column(Date, nullable=True)
    shipment_eta                  = Column(Date, nullable=True)
    receive_shipping_docs_status  = Column(SAEnum(DocReceiveStatusEnum, name="doc_receive_status_enum"), nullable=True)
    receive_shipping_docs_date    = Column(Date, nullable=True)
    delivery_approval_date        = Column(Date, nullable=True)
    customs_exemption_date        = Column(Date, nullable=True)
    cd_to_clearing_agent_date     = Column(Date, nullable=True)
    asn_no                        = Column(String(100), nullable=True)
    asn_date                      = Column(Date, nullable=True)
    delivery_email_date           = Column(Date, nullable=True)
    delivery_note_no              = Column(String(100), nullable=True)
    dn_date                       = Column(Date, nullable=True)
    gate_pass_creation_date       = Column(Date, nullable=True)

    lot                           = relationship("LotMonitoring", back_populates="delivery_procedures")
    order_item                    = relationship("OrderItemDetail", back_populates="delivery_procedures")

    def __repr__(self) -> str:
        return (
            f"<DeliveryProcedure(dp_id={self.dp_id!r}, lot_id={self.lot_id!r}, "
            f"order_item_detail_id={self.order_item_detail_id!r})>"
        )
