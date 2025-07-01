from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class OrderEvent(Base):
    __tablename__ = "order_events"

    order_event_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id       = Column(
        Integer,
        ForeignKey("order_details.order_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    event_date           = Column(Date, nullable=False, index=True)
    event          = Column(String(255), nullable=False)
    remarks        = Column(Text, nullable=True)

    order          = relationship("OrderDetail", back_populates="events")

    def __repr__(self) -> str:
        return (
            f"<OrderEvent(id={self.order_event_id!r}, "
            f"order_id={self.order_id!r}, date={self.date!r}, event={self.event!r})>"
        )
