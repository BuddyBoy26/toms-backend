from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from datetime import date
from decimal import Decimal

# Reusable types
Decimal14 = Annotated[Decimal, Field(..., max_digits=14, decimal_places=2)]
OptionalDecimal14 = Optional[Annotated[Decimal, Field(None, max_digits=14, decimal_places=2)]]
DateOpt = Optional[date]
IntOpt = Optional[int]
StrOpt = Optional[str]

class LotMonitoringBase(BaseModel):
    order_item_detail_id: int
    shipment_no: StrOpt = None
    item_lot_no: StrOpt = None
    item_unit_price: Decimal = Decimal14
    quantity: Decimal = Decimal14
    item_total_value: Decimal = Decimal14
    contractual_delivery_date: DateOpt = None
    inspection_call_date_tent: DateOpt = None
    inspection_call_date_act: DateOpt = None
    inspection_date_advised: DateOpt = None
    no_of_inspection_days: IntOpt = None
    actual_inspection_date: DateOpt = None
    inspection_delay_days: IntOpt = None
    units_inspected: IntOpt = None
    mom_received_date: DateOpt = None
    dispatch_clearance_date: DateOpt = None
    dispatch_clearance_delay: IntOpt = None
    asn_date: DateOpt = None
    actual_delivery_date: DateOpt = None
    delivery_note_no: StrOpt = None
    delivered_quantity: IntOpt = None
    pending_lot_id: IntOpt = None
    goods_receipt_no: StrOpt = None
    delivery_delay_days: IntOpt = None
    delay_by_dewa: IntOpt = None
    other_delay_by_dewa: IntOpt = None
    total_ld_delay: IntOpt = None
    invoice_nos: StrOpt = None
    invoice_dates: StrOpt = None
    invoice_values: StrOpt = None
    srm_invoice_no: StrOpt = None
    contractual_payment_date: DateOpt = None
    payment_amount_received: OptionalDecimal14 = None
    payment_received_date: DateOpt = None
    commission_calculated: OptionalDecimal14 = None
    commission_invoice_no: StrOpt = None
    commission_invoice_date: DateOpt = None
    commission_received_date: DateOpt = None
    shipment_arrival_notice: DateOpt = None
    shipment_arrival_actual: DateOpt = None
    delivery_auth_application: DateOpt = None
    delay_in_authorisation_days: IntOpt = None
    gatepass_date: DateOpt = None
    payment_application_date: DateOpt = None
    revised_date: DateOpt = None

class LotMonitoringCreate(LotMonitoringBase):
    """All fields may be provided by client."""
    pass

class LotMonitoringUpdate(BaseModel):
    order_item_detail_id: IntOpt = None
    shipment_no: StrOpt = None
    item_lot_no: StrOpt = None
    item_unit_price: OptionalDecimal14 = None
    quantity: OptionalDecimal14 = None
    item_total_value: OptionalDecimal14 = None
    contractual_delivery_date: DateOpt = None
    inspection_call_date_tent: DateOpt = None
    inspection_call_date_act: DateOpt = None
    inspection_date_advised: DateOpt = None
    no_of_inspection_days: IntOpt = None
    actual_inspection_date: DateOpt = None
    inspection_delay_days: IntOpt = None
    units_inspected: IntOpt = None
    mom_received_date: DateOpt = None
    dispatch_clearance_date: DateOpt = None
    dispatch_clearance_delay: IntOpt = None
    asn_date: DateOpt = None
    actual_delivery_date: DateOpt = None
    delivery_note_no: StrOpt = None
    delivered_quantity: IntOpt = None
    pending_lot_id: IntOpt = None
    goods_receipt_no: StrOpt = None
    delivery_delay_days: IntOpt = None
    delay_by_dewa: IntOpt = None
    other_delay_by_dewa: IntOpt = None
    total_ld_delay: IntOpt = None
    invoice_nos: StrOpt = None
    invoice_dates: StrOpt = None
    invoice_values: StrOpt = None
    srm_invoice_no: StrOpt = None
    contractual_payment_date: DateOpt = None
    payment_amount_received: OptionalDecimal14 = None
    payment_received_date: DateOpt = None
    commission_calculated: OptionalDecimal14 = None
    commission_invoice_no: StrOpt = None
    commission_invoice_date: DateOpt = None
    commission_received_date: DateOpt = None
    shipment_arrival_notice: DateOpt = None
    shipment_arrival_actual: DateOpt = None
    delivery_auth_application: DateOpt = None
    delay_in_authorisation_days: IntOpt = None
    gatepass_date: DateOpt = None
    payment_application_date: DateOpt = None
    revised_date: DateOpt = None

class LotMonitoringRead(LotMonitoringBase):
    lot_id: int  # This is an Integer autoincrement in the model, not a string

    class Config:
        from_attributes = True