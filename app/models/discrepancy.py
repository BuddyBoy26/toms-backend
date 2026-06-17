# models/discrepancy.py
from sqlalchemy import (
    Column, String, Date, Integer, JSON, ForeignKey
)
from sqlalchemy.orm import relationship
from ..database import Base

class Discrepancy(Base):
    __tablename__ = "discrepancies"

    discrepancy_id         = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lot_id                 = Column(
        Integer,
        ForeignKey("lot_monitoring.lot_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Header Information
    dewa_letter_ref        = Column(String(100), nullable=True)
    letter_date            = Column(Date, nullable=True)
    total_discrepant_units = Column(Integer, nullable=True)

    # Array of rows stored as a JSON object
    # Format: [{"qty": 1, "nature_of_discrepancy": "Broken", "remarks": "...", "pending_status": true, ...}]
    details                = Column(JSON, nullable=False)

    lot                    = relationship("LotMonitoring", back_populates="discrepancies")

    def __repr__(self) -> str:
        return (
            f"<Discrepancy(id={self.discrepancy_id!r}, lot_id={self.lot_id!r}, "
            f"dewa_letter_ref={self.dewa_letter_ref!r})>"
        )