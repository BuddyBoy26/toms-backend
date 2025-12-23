from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import date

DateOpt = Optional[date]
IntOpt = Optional[int]
StrOpt = Optional[str]

class DeliveryProcedureBase(BaseModel):
    lot_id: int
    order_item_detail_id: int

    item_no_dewa: StrOpt = None
    lot_no_dewa: StrOpt = None
    shipment_no: StrOpt = None

    # Shipment dates
    shipment_etd: DateOpt = None
    shipment_eta: DateOpt = None
    shipment_atd: DateOpt = None
    shipment_ata: DateOpt = None

    # Document status
    document_status: IntOpt = None  # 0,1,2
    remarks_document_status: StrOpt = None
    receive_shipping_docs_date: DateOpt = None

    # CD Exemption
    cd_exemption: IntOpt = None     # 0,1
    cd_exemption_submitted: DateOpt = None
    cd_exemption_recieved_date: DateOpt = None

    # CEPA / DDU
    cepa_ddu: IntOpt = None         # 0,1
    cepa_ddu_date: DateOpt = None

    # Processing
    authorization_letter_date: DateOpt = None
    bl_stamped_date: DateOpt = None
    documents_to_agent_date: DateOpt = None

    # ASN
    asn_no: StrOpt = None
    asn_date: DateOpt = None
    delivery_intimation_date: DateOpt = None
    deliver_approval_from_stores_date: DateOpt = None

    # Delivery note & gate pass
    delivery_note_no: StrOpt = None
    delivery_note_date: DateOpt = None
    gate_pass_request_date: DateOpt = None
    gate_pass_received_date: DateOpt = None

    # Final delivery
    delivery_date: DateOpt = None
    delivery_date_smart_meters: DateOpt = None
    end_of_delivery_remarks: StrOpt = None

class DeliveryProcedureCreate(DeliveryProcedureBase):
    """All fields allowed on create."""
    pass

class DeliveryProcedureUpdate(BaseModel):
    lot_id: IntOpt = None
    order_item_detail_id: IntOpt = None

    item_no_dewa: StrOpt = None
    lot_no_dewa: StrOpt = None
    shipment_no: StrOpt = None

    shipment_etd: DateOpt = None
    shipment_eta: DateOpt = None
    shipment_atd: DateOpt = None
    shipment_ata: DateOpt = None

    document_status: IntOpt = None
    remarks_document_status: StrOpt = None
    receive_shipping_docs_date: DateOpt = None

    cd_exemption: IntOpt = None
    cd_exemption_submitted: DateOpt = None
    cd_exemption_recieved_date: DateOpt = None

    cepa_ddu: IntOpt = None
    cepa_ddu_date: DateOpt = None

    authorization_letter_date: DateOpt = None
    bl_stamped_date: DateOpt = None
    documents_to_agent_date: DateOpt = None

    asn_no: StrOpt = None
    asn_date: DateOpt = None
    delivery_intimation_date: DateOpt = None
    deliver_approval_from_stores_date: DateOpt = None

    delivery_note_no: StrOpt = None
    delivery_note_date: DateOpt = None
    gate_pass_request_date: DateOpt = None
    gate_pass_received_date: DateOpt = None

    delivery_date: DateOpt = None
    delivery_date_smart_meters: DateOpt = None
    end_of_delivery_remarks: StrOpt = None

class DeliveryProcedureRead(DeliveryProcedureBase):
    dp_id: int

    class Config:
        from_attributes = True
