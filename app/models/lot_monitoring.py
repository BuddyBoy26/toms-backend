from sqlalchemy import (
    Column, Integer, String, Date, Numeric, ForeignKey
)
from sqlalchemy.orm import relationship
from ..database import Base

class LotMonitoring(Base):
    __tablename__ = "lot_monitoring"

    lot_id                      = Column(String(20), primary_key=True, index=True)
    order_item_detail_id        = Column(
        Integer,
        ForeignKey("order_item_details.order_item_detail_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    shipment_no                 = Column(String(50), nullable=True)
    item_lot_no                 = Column(String(50), nullable=True)
    item_unit_price             = Column(Numeric(14,2), nullable=False)
    item_total_value            = Column(Numeric(14,2), nullable=False)
    contractual_delivery_date   = Column(Date, nullable=True)
    inspection_call_date_tent   = Column(Date, nullable=True)
    inspection_call_date_act    = Column(Date, nullable=True)
    inspection_date_advised     = Column(Date, nullable=True)
    no_of_inspection_days       = Column(Integer, nullable=True)
    actual_inspection_date      = Column(Date, nullable=True)
    inspection_delay_days       = Column(Integer, nullable=True)
    units_inspected             = Column(Integer, nullable=True)
    mom_received_date           = Column(Date, nullable=True)
    dispatch_clearance_date     = Column(Date, nullable=True)
    dispatch_clearance_delay    = Column(Integer, nullable=True)
    asn_date                    = Column(Date, nullable=True)
    actual_delivery_date        = Column(Date, nullable=True)
    delivery_note_no            = Column(String(100), nullable=True)
    delivered_quantity          = Column(Integer, nullable=True)
    pending_lot_id              = Column(String(20), nullable=True)
    goods_receipt_no            = Column(String(100), nullable=True)
    delivery_delay_days         = Column(Integer, nullable=True)
    delay_by_dewa               = Column(Integer, nullable=True)
    other_delay_by_dewa         = Column(Integer, nullable=True)
    total_ld_delay              = Column(Integer, nullable=True)
    invoice_nos                 = Column(String(200), nullable=True)
    invoice_dates               = Column(String(200), nullable=True)  # comma-separated or JSON
    invoice_values              = Column(String(200), nullable=True)
    srm_invoice_no              = Column(String(100), nullable=True)
    contractual_payment_date    = Column(Date, nullable=True)
    payment_amount_received     = Column(Numeric(14,2), nullable=True)
    payment_received_date       = Column(Date, nullable=True)
    commission_calculated       = Column(Numeric(14,2), nullable=True)
    commission_invoice_no       = Column(String(100), nullable=True)
    commission_invoice_date     = Column(Date, nullable=True)
    commission_received_date    = Column(Date, nullable=True)
    shipment_arrival_notice     = Column(Date, nullable=True)
    shipment_arrival_actual     = Column(Date, nullable=True)
    delivery_auth_application   = Column(Date, nullable=True)
    delay_in_authorisation_days = Column(Integer, nullable=True)
    gatepass_date               = Column(Date, nullable=True)
    payment_application_date    = Column(Date, nullable=True)
    revised_date                = Column(Date, nullable=True)

    order_item_detail = relationship("OrderItemDetail", back_populates="lot_monitorings")

    def __repr__(self) -> str:
        return f"<LotMonitoring(lot_id={self.lot_id!r}, order_item_detail_id={self.order_item_detail_id!r})>"
