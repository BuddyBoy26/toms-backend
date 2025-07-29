from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from ..database import Base

class DrawingDetails(Base):
    __tablename__ = "drawing_details"
    __table_args__ = (
        UniqueConstraint("tender_no", "order_id", name="uq_tender_order"),
    )

    id = Column(Integer, primary_key=True, index=True)
    tender_no = Column(String, ForeignKey("tenders.tender_no"), nullable=False)
    order_id = Column(Integer, ForeignKey("order_details.order_id"), nullable=False)

    drawing_no = Column(String, nullable=True)
    drawing_version = Column(String, nullable=True)
    submission_date = Column(Date, nullable=True)
    revision = Column(String, nullable=True)      # “Drawing Revision No and/or Version”
    approval_date = Column(Date, nullable=True)
    sent_date = Column(Date, nullable=True)       # “Drawing sent … to Principals Date”

    # relationships (optional, adjust your models’ class names if different)
    tender = relationship("Tender", back_populates="drawings")
    order = relationship("OrderDetail", back_populates="drawings")
