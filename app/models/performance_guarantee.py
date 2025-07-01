import enum
from sqlalchemy import (
    Column, Integer, String, Date, Numeric, Text,
    ForeignKey, ARRAY, Enum
)
from sqlalchemy.orm import relationship
from ..database import Base

class PBGStatusEnum(str, enum.Enum):
    NOT_ISSUED         = "NOT Issued"
    ISSUED_EXTENDED    = "Issued / Extended"
    EXTENSION_REQUIRED = "Extension Required"
    NOT_RELEASED       = "NOT Released"
    RELEASED           = "Released"

class PerformanceGuarantee(Base):
    __tablename__ = "performance_guarantees"

    pg_id                    = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id                 = Column(
        Integer,
        ForeignKey("order_details.order_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    pg_no                    = Column(String(100), nullable=False, index=True)
    pg_issuing_bank          = Column(String(100), nullable=True)
    pg_deposit_receipt_no    = Column(String(100), nullable=True)
    cheque_no                = Column(String(50),  nullable=True)
    tt_date                  = Column(Date, nullable=True)
    document_date            = Column(Date, nullable=True)
    pg_value                 = Column(Numeric(12,2), nullable=False)
    pg_expiry_date           = Column(Date, nullable=False)
    pg_submitted_date        = Column(Date, nullable=True)
    pg_return_date           = Column(Date, nullable=True)
    pg_release_date_dewa     = Column(Date, nullable=True)
    pg_release_date_bank     = Column(Date, nullable=True)
    pg_extension_dates       = Column(ARRAY(Date), nullable=True)
    remarks                  = Column(Text, nullable=True)
    pending_status           = Column(
                                 Enum(PBGStatusEnum, name="pbg_status_enum"),
                                 nullable=False,
                                 default=PBGStatusEnum.NOT_ISSUED
                               )

    order                    = relationship("OrderDetail", back_populates="performance_guarantees")

    def __repr__(self) -> str:
        return (
            f"<PerformanceGuarantee(pg_id={self.pg_id!r}, "
            f"order_id={self.order_id!r}, pg_no={self.pg_no!r}, "
            f"pending_status={self.pending_status!r})>"
        )
