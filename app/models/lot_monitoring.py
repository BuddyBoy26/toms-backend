from sqlalchemy import (
    Column, Integer, String, Date, Numeric, ForeignKey
)
from sqlalchemy.orm import relationship
from ..database import Base

class LotMonitoring(Base):
    __tablename__ = "lot_monitoring"

    # HEADING: Lot Monitoring Information

    lot_id                      = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # ONLY TWO FOREIGN KEYS - as requested
    order_id                    = Column(
        Integer, 
        ForeignKey("order_details.order_id", ondelete="NO ACTION"), 
        nullable=False,
        index=True
    )
    order_item_detail_id        = Column(
        Integer,
        ForeignKey("order_item_details.order_item_detail_id", ondelete="NO ACTION"),
        nullable=False,
        index=True,
    )
    
    # REGULAR COLUMNS - No foreign keys, populated via dropdowns in frontend
    order_description           = Column(String(500), nullable=True)  # Populated from order_details dropdown
    shipment_no                 = Column(String(50), nullable=True)
    item_lot_no                 = Column(String(50), nullable=True)
    item_unit_price             = Column(Numeric(14, 4), nullable=False)
    currency                    = Column(String(10), nullable=False)
    quantity                    = Column(Numeric(14, 4), nullable=False)
    item_total_value            = Column(Numeric(14, 4), nullable=False)
    po_line_no                  = Column(String(50), nullable=True)
    weeks                       = Column(Integer, nullable=True)
    contractual_delivery_date   = Column(Date, nullable=True)

    # Heading: Inspection

    # SUBHEADING: Before Inspection
    inspection_call_date_tent   = Column(Date, nullable=True)
    inspection_call_date_act    = Column(Date, nullable=True)
    inspection_date_advised     = Column(Date, nullable=True)
    no_of_inspection_days       = Column(Integer, nullable=True) 
    inspection_at               = Column(String(100), nullable=True)
    actual_inspection_date      = Column(Date, nullable=True)
    
    # SUBHEADING: After Inspection
    units_inspected             = Column(Integer, nullable=True)
    after_inspection_pending_quantity = Column(Integer, nullable=True)
    after_inspection_pending_lot_id   = Column(Integer, nullable=True)  # No FK - just stores the ID
    mom_date                    = Column(Date, nullable=True)
    dispatch_clearance_date     = Column(Date, nullable=True)
    inspection_delay_days       = Column(Integer, nullable=True)
    dispatch_clearance_delay    = Column(Integer, nullable=True)

    # Heading: Shipment Details
    etd_date                    = Column(Date, nullable=True)
    actual_dispatch_date        = Column(Date, nullable=True)
    eta_date                    = Column(Date, nullable=True)
    actual_arrival_date         = Column(Date, nullable=True)

    # Heading: Delivery Authorisation
    requested_delivery_date     = Column(Date, nullable=True)
    customs_duty_exemption_date = Column(Date, nullable=True)
    asn_date                    = Column(Date, nullable=True)

    # Heading: Delivery Details
    actual_delivery_date        = Column(Date, nullable=True)
    meter_delivery_date         = Column(Date, nullable=True)
    delivery_note_no            = Column(String(100), nullable=True)
    delivered_quantity          = Column(Integer, nullable=True)
    pending_quantity            = Column(Integer, nullable=True)
    remarks_on_delivery         = Column(String(500), nullable=True)
    delivery_total_value        = Column(Numeric(14, 4), nullable=True)
    grn_no                      = Column(String(100), nullable=True)
    pending_lot_id              = Column(Integer, nullable=True)  # No FK - just stores the ID

    # Heading: Delay Details
    main_units_delay_days       = Column(Integer, nullable=True)
    accessories_delay_days      = Column(Integer, nullable=True)
    delay_by_dewa               = Column(Integer, nullable=True)
    other_delay_by_dewa         = Column(Integer, nullable=True)
    reason_for_other_delay      = Column(String(500), nullable=True)

    # Heading: Payment Details
    contractual_payment_date    = Column(Date, nullable=True)
    invoice_no                  = Column(String(100), nullable=True)
    invoice_date                = Column(Date, nullable=True)
    invoice_value               = Column(Numeric(14, 4), nullable=True)
    srm_invoice_no              = Column(String(100), nullable=True)
    srm_invoice_date            = Column(Date, nullable=True)
    srm_invoice_value           = Column(Numeric(14, 4), nullable=True)
    payment_amount_received     = Column(Numeric(14, 4), nullable=True)
    payment_received_date       = Column(Date, nullable=True)
    delay_in_payment_days       = Column(Integer, nullable=True)
    reason_for_payment_delay    = Column(String(500), nullable=True)

    # Heading: Commission Details
    commission_amount_for_lot   = Column(Numeric(14, 4), nullable=True)
    commission_amount_for_delivered_quantity = Column(Numeric(14, 4), nullable=True)
    commission_invoice_no       = Column(String(100), nullable=True)
    commission_invoice_date     = Column(Date, nullable=True)
    commission_recieved_date     = Column(Date, nullable=True)
    commission_amount_invoiced  = Column(Numeric(14, 4), nullable=True)
    balance_commission_amount   = Column(Numeric(14, 4), nullable=True)

    # Heading: Summary for LD Calculation
    ld_delay_units_or_meters    = Column(Integer, nullable=True)  # 0 for units, 1 for meters
    ld_delay_units              = Column(Integer, nullable=True)
    ld_delay_meters             = Column(Integer, nullable=True)

    # Subheading: Miscellaneous Delays
    delay_dewa_authorisation_days = Column(Integer, nullable=True)
    remarks_delay               = Column(String(500), nullable=True)
    force_majeure               = Column(Integer, nullable=True)
    force_majeure_days          = Column(Integer, nullable=True)

    actual_delay_for_ld         = Column(Integer, nullable=True)
    actual_ld_amount            = Column(Numeric(14, 4), nullable=True)
    max_ld_amount               = Column(Numeric(14, 4), nullable=True)
    chargeable_ld_amount        = Column(Numeric(14, 4), nullable=True)

    # Relationships - Only for the two foreign keys
    order_item_detail = relationship("OrderItemDetail", back_populates="lot_monitorings")
    order = relationship("OrderDetail", back_populates="lots")
    
    # Child relationships
    discrepancies = relationship(
        "Discrepancy",
        back_populates="lot",
        cascade="all, delete-orphan",
    )
    liquidated_damages = relationship(
        "LiquidatedDamages",
        back_populates="lot",
        cascade="all, delete-orphan",
    )
    delivery_procedures = relationship(
        "DeliveryProcedure",
        back_populates="lot",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<LotMonitoring(lot_id={self.lot_id!r}, order_item_detail_id={self.order_item_detail_id!r})>"