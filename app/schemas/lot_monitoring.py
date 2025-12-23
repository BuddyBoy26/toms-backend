from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from datetime import date
from decimal import Decimal

# Reusable types
Decimal14 = Annotated[Decimal, Field(..., max_digits=14, decimal_places=4)]
OptionalDecimal14 = Optional[Annotated[Decimal, Field(None, max_digits=14, decimal_places=4)]]
DateOpt = Optional[date]
IntOpt = Optional[int]
StrOpt = Optional[str]

class LotMonitoringBase(BaseModel):
    # Lot Monitoring Information
    order_item_detail_id: int
    order_id: int
    order_description: StrOpt = None
    shipment_no: StrOpt = None
    item_lot_no: StrOpt = None
    item_unit_price: Decimal = Decimal14
    currency: str
    quantity: Decimal = Decimal14
    item_total_value: Decimal = Decimal14
    po_line_no: StrOpt = None
    contractual_delivery_date: DateOpt = None

    # Inspection - Before Inspection
    inspection_call_date_tent: DateOpt = None
    inspection_call_date_act: DateOpt = None
    inspection_date_advised: DateOpt = None
    no_of_inspection_days: IntOpt = None
    inspection_at: StrOpt = None
    actual_inspection_date: DateOpt = None

    # Inspection - After Inspection
    units_inspected: IntOpt = None
    after_inspection_pending_quantity: IntOpt = None
    after_inspection_pending_lot_id: IntOpt = None
    mom_date: DateOpt = None
    dispatch_clearance_date: DateOpt = None
    inspection_delay_days: IntOpt = None
    dispatch_clearance_delay: IntOpt = None

    # Shipment Details
    etd_date: DateOpt = None
    actual_dispatch_date: DateOpt = None
    eta_date: DateOpt = None
    actual_arrival_date: DateOpt = None

    # Delivery Authorisation
    requested_delivery_date: DateOpt = None
    customs_duty_exemption_date: DateOpt = None
    asn_date: DateOpt = None

    # Delivery Details
    actual_delivery_date: DateOpt = None
    meter_delivery_date: DateOpt = None
    delivery_note_no: StrOpt = None
    delivered_quantity: IntOpt = None
    pending_quantity: IntOpt = None
    remarks_on_delivery: StrOpt = None
    delivery_total_value: OptionalDecimal14 = None
    grn_no: StrOpt = None
    pending_lot_id: IntOpt = None

    # Delay Details
    main_units_delay_days: IntOpt = None
    accessories_delay_days: IntOpt = None
    delay_by_dewa: IntOpt = None
    other_delay_by_dewa: IntOpt = None
    reason_for_other_delay: StrOpt = None

    # Payment Details
    contractual_payment_date: DateOpt = None
    invoice_no: StrOpt = None
    invoice_date: DateOpt = None
    invoice_value: OptionalDecimal14 = None
    srm_invoice_no: StrOpt = None
    srm_invoice_date: DateOpt = None
    srm_invoice_value: OptionalDecimal14 = None
    payment_amount_received: OptionalDecimal14 = None
    payment_received_date: DateOpt = None
    delay_in_payment_days: IntOpt = None
    reason_for_payment_delay: StrOpt = None

    # Commission Details
    commission_amount_for_lot: OptionalDecimal14 = None
    commission_amount_for_delivered_quantity: OptionalDecimal14 = None
    commission_invoice_no: StrOpt = None
    commission_invoice_date: DateOpt = None
    commission_amount_invoiced: OptionalDecimal14 = None
    balance_commission_amount: OptionalDecimal14 = None

    # Summary for LD calculation
    ld_delay_units_or_meters: IntOpt = None  # 0 for units, 1 for meters
    ld_delay_units: IntOpt = None
    ld_delay_meters: IntOpt = None

    # Miscellaneous delays
    delay_dewa_authorisation_days: IntOpt = None
    remarks_delay: StrOpt = None
    force_majeure: IntOpt = None
    force_majeure_days: IntOpt = None

    actual_delay_for_ld: IntOpt = None
    actual_ld_amount: OptionalDecimal14 = None
    max_ld_amount: OptionalDecimal14 = None
    chargeable_ld_amount: OptionalDecimal14 = None

class LotMonitoringCreate(LotMonitoringBase):
    """All fields may be provided by client."""
    pass

class LotMonitoringUpdate(BaseModel):
    order_item_detail_id: IntOpt = None
    order_id: IntOpt = None
    order_description: StrOpt = None
    shipment_no: StrOpt = None
    item_lot_no: StrOpt = None
    item_unit_price: OptionalDecimal14 = None
    currency: StrOpt = None
    quantity: OptionalDecimal14 = None
    item_total_value: OptionalDecimal14 = None
    po_line_no: StrOpt = None
    contractual_delivery_date: DateOpt = None

    # Inspection - Before Inspection
    inspection_call_date_tent: DateOpt = None
    inspection_call_date_act: DateOpt = None
    inspection_date_advised: DateOpt = None
    no_of_inspection_days: IntOpt = None
    inspection_at: StrOpt = None
    actual_inspection_date: DateOpt = None

    # Inspection - After Inspection
    units_inspected: IntOpt = None
    after_inspection_pending_quantity: IntOpt = None
    after_inspection_pending_lot_id: IntOpt = None
    mom_date: DateOpt = None
    dispatch_clearance_date: DateOpt = None
    inspection_delay_days: IntOpt = None
    dispatch_clearance_delay: IntOpt = None

    # Shipment Details
    etd_date: DateOpt = None
    actual_dispatch_date: DateOpt = None
    eta_date: DateOpt = None
    actual_arrival_date: DateOpt = None

    # Delivery Authorisation
    requested_delivery_date: DateOpt = None
    customs_duty_exemption_date: DateOpt = None
    asn_date: DateOpt = None

    # Delivery Details
    actual_delivery_date: DateOpt = None
    meter_delivery_date: DateOpt = None
    delivery_note_no: StrOpt = None
    delivered_quantity: IntOpt = None
    pending_quantity: IntOpt = None
    remarks_on_delivery: StrOpt = None
    delivery_total_value: OptionalDecimal14 = None
    grn_no: StrOpt = None
    pending_lot_id: IntOpt = None

    # Delay Details
    main_units_delay_days: IntOpt = None
    accessories_delay_days: IntOpt = None
    delay_by_dewa: IntOpt = None
    other_delay_by_dewa: IntOpt = None
    reason_for_other_delay: StrOpt = None

    # Payment Details
    contractual_payment_date: DateOpt = None
    invoice_no: StrOpt = None
    invoice_date: DateOpt = None
    invoice_value: OptionalDecimal14 = None
    srm_invoice_no: StrOpt = None
    srm_invoice_date: DateOpt = None
    srm_invoice_value: OptionalDecimal14 = None
    payment_amount_received: OptionalDecimal14 = None
    payment_received_date: DateOpt = None
    delay_in_payment_days: IntOpt = None
    reason_for_payment_delay: StrOpt = None

    # Commission Details
    commission_amount_for_lot: OptionalDecimal14 = None
    commission_amount_for_delivered_quantity: OptionalDecimal14 = None
    commission_invoice_no: StrOpt = None
    commission_invoice_date: DateOpt = None
    commission_amount_invoiced: OptionalDecimal14 = None
    balance_commission_amount: OptionalDecimal14 = None

    # Summary for LD calculation
    ld_delay_units_or_meters: IntOpt = None
    ld_delay_units: IntOpt = None
    ld_delay_meters: IntOpt = None

    # Miscellaneous delays
    delay_dewa_authorisation_days: IntOpt = None
    remarks_delay: StrOpt = None
    force_majeure: IntOpt = None
    force_majeure_days: IntOpt = None

    actual_delay_for_ld: IntOpt = None
    actual_ld_amount: OptionalDecimal14 = None
    max_ld_amount: OptionalDecimal14 = None
    chargeable_ld_amount: OptionalDecimal14 = None

class LotMonitoringRead(LotMonitoringBase):
    lot_id: int  # This is an Integer autoincrement in the model, not a string

    class Config:
        from_attributes = True