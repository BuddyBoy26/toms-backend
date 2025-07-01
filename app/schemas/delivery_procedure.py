from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from app.models.delivery_procedure import DocReceiveStatusEnum

class DeliveryProcedureBase(BaseModel):
    lot_id: str
    order_item_detail_id: int
    shipment_etd: Optional[date] = None
    shipment_eta: Optional[date] = None
    receive_shipping_docs_status: Optional[DocReceiveStatusEnum] = None
    receive_shipping_docs_date: Optional[date] = None
    delivery_approval_date: Optional[date] = None
    customs_exemption_date: Optional[date] = None
    cd_to_clearing_agent_date: Optional[date] = None
    asn_no: Optional[str] = None
    asn_date: Optional[date] = None
    delivery_email_date: Optional[date] = None
    delivery_note_no: Optional[str] = None
    dn_date: Optional[date] = None
    gate_pass_creation_date: Optional[date] = None

class DeliveryProcedureCreate(DeliveryProcedureBase):
    """Client supplies all except dp_id."""

class DeliveryProcedureUpdate(BaseModel):
    shipment_etd: Optional[date] = None
    shipment_eta: Optional[date] = None
    receive_shipping_docs_status: Optional[DocReceiveStatusEnum] = None
    receive_shipping_docs_date: Optional[date] = None
    delivery_approval_date: Optional[date] = None
    customs_exemption_date: Optional[date] = None
    cd_to_clearing_agent_date: Optional[date] = None
    asn_no: Optional[str] = None
    asn_date: Optional[date] = None
    delivery_email_date: Optional[date] = None
    delivery_note_no: Optional[str] = None
    dn_date: Optional[date] = None
    gate_pass_creation_date: Optional[date] = None

class DeliveryProcedureRead(DeliveryProcedureBase):
    dp_id: int

    class Config:
        from_attributes = True
