from sqlalchemy import (
    Column, String, Date, Integer, Boolean, Text, ForeignKey
)
from sqlalchemy.orm import relationship
from ..database import Base

class Discrepancy(Base):
    __tablename__ = "discrepancies"

    discrepancy_id      = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lot_id              = Column(
        String(20),
        ForeignKey("lot_monitoring.lot_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    dewa_letter_ref     = Column(String(100), nullable=False)
    letter_date         = Column(Date, nullable=False)
    pending_quantity    = Column(Integer, nullable=True)
    unit_sl_nos         = Column(String(200), nullable=True)
    discrepancies       = Column(Text, nullable=False)
    remarks             = Column(Text, nullable=True)
    pending_status      = Column(Boolean, nullable=False, default=True)
    resolution_date     = Column(Date, nullable=True)
    delivery_note_no    = Column(String(100), nullable=True)
    actual_delivery_date= Column(Date, nullable=True)

    lot                 = relationship("LotMonitoring", back_populates="discrepancies")

    def __repr__(self) -> str:
        return (
            f"<Discrepancy(id={self.discrepancy_id!r}, lot_id={self.lot_id!r}, "
            f"dewa_letter_ref={self.dewa_letter_ref!r})>"
        )
