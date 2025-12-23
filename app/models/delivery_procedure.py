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
    
    # ONLY TWO FOREIGN KEYS - as requested
    lot_id                        = Column(
        Integer,
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
    
    # REGULAR COLUMNS - No foreign keys, populated via dropdowns in frontend
    item_no_dewa                  = Column(String(100), nullable=True)  # Populated from order_item_details
    lot_no_dewa                   = Column(String(50), nullable=True)   # Populated from lot_monitoring
    shipment_no                = Column(String(50), nullable=True)   # Populated from lot_monitoring

    # Shipment Dates - Just regular date columns
    shipment_etd                  = Column(Date, nullable=True)         # Populated from lot_monitoring
    shipment_eta                  = Column(Date, nullable=True)         # Populated from lot_monitoring
    shipment_atd                  = Column(Date, nullable=True)         # Populated from lot_monitoring
    shipment_ata                  = Column(Date, nullable=True)         # Populated from lot_monitoring

    # dispatch_clearance_date       = Column(Date, nullable=True)         # Populated from lot_monitoring
    # shipment_eta                  = Column(Date, nullable=True)         # Populated from lot_monitoring
    # actual_dispatch_date          = Column(Date, nullable=True)         # Populated from lot_monitoring
    
    # Document Status
    document_status               = Column(Integer, nullable=True)      # 0: Not received, 1: Partial, 2: All received
    remarks_document_status       = Column(String(500), nullable=True)
    receive_shipping_docs_date    = Column(Date, nullable=True)         # If partial or all received
    
    # CD Exemption
    cd_exemption                  = Column(Integer, nullable=True)      # 0: Not Exempted, 1: Exempted
    cd_exemption_submitted        = Column(Date, nullable=True)         # Date of submission to CD department
    cd_exemption_recieved_date    = Column(Date, nullable=True)
    
    # CEPA/DDU
    cepa_ddu                      = Column(Integer, nullable=True)      # 0: CEPA, 1: DDU
    cepa_ddu_date                 = Column(Date, nullable=True)
    
    # Submission & Processing
    authorization_letter_date                 = Column(Date, nullable=True)
    bl_stamped_date               = Column(Date, nullable=True)
    documents_to_agent_date       = Column(Date, nullable=True)
    
    # ASN Details
    asn_no                        = Column(String(100), nullable=True)
    asn_date                      = Column(Date, nullable=True)         # Populated from lot_monitoring
    delivery_intimation_date      = Column(Date, nullable=True)
    deliver_approval_from_stores_date = Column(Date, nullable=True)
    
    # Delivery Note & Gate Pass
    delivery_note_no              = Column(String(100), nullable=True)
    delivery_note_date            = Column(Date, nullable=True)
    gate_pass_request_date        = Column(Date, nullable=True)
    gate_pass_received_date       = Column(Date, nullable=True)
    
    # Final Delivery
    delivery_date                 = Column(Date, nullable=True)
    delivery_date_smart_meters    = Column(Date, nullable=True)
    end_of_delivery_remarks       = Column(String(500), nullable=True)
    
    # Relationships - Only for the two foreign keys
    lot                           = relationship("LotMonitoring", back_populates="delivery_procedures")
    order_item                    = relationship("OrderItemDetail", back_populates="delivery_procedures")

    def __repr__(self) -> str:
        return (
            f"<DeliveryProcedure(dp_id={self.dp_id!r}, lot_id={self.lot_id!r}, "
            f"order_item_detail_id={self.order_item_detail_id!r})>"
        )