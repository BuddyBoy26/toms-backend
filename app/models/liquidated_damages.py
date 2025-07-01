from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, ARRAY
)
from sqlalchemy.orm import relationship
from ..database import Base

class LiquidatedDamages(Base):
    __tablename__ = "liquidated_damages"

    ld_id                     = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lot_id                    = Column(
        String(20),
        ForeignKey("lot_monitoring.lot_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lot_qty                   = Column(Integer, nullable=False)
    actual_delivery_date      = Column(Date, nullable=True)
    quantities_delivered      = Column(ARRAY(Integer), nullable=False)
    delivery_delays_days      = Column(ARRAY(Integer), nullable=False)

    lot                        = relationship(
        "LotMonitoring",
        back_populates="liquidated_damages"
    )

    def __repr__(self) -> str:
        return (
            f"<LiquidatedDamages(id={self.ld_id!r}, lot_id={self.lot_id!r})>"
        )
