from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class OrderItemDetail(Base):
    __tablename__ = "order_item_details"

    order_item_detail_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id             = Column(
        Integer,
        ForeignKey("order_details.order_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    item_id              = Column(
        Integer,
        ForeignKey("item_master.item_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    item_description     = Column(String(500), nullable=True)
    item_no_dewa         = Column(String(100), nullable=False)
    item_quantity        = Column(Integer, nullable=False)
    item_unit_price      = Column(Numeric(14,2), nullable=False)
    number_of_lots       = Column(Integer, nullable=False)

    order        = relationship("OrderDetail",     back_populates="items")
    item_master  = relationship("ItemMaster",      back_populates="order_items")
    lot_monitorings = relationship(
        "LotMonitoring",
        back_populates="order_item_detail",
        cascade="all, delete-orphan",
    )
    delivery_procedures = relationship(
        "DeliveryProcedure",
        back_populates="order_item",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<OrderItemDetail("
            f"id={self.order_item_detail_id!r}, "
            f"order_id={self.order_id!r}, "
            f"item_id={self.item_id!r})>"
        )
