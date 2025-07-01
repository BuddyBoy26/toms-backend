import enum
from sqlalchemy import (
    Column, Integer, String, Date, Numeric, Text,
    ForeignKey, ARRAY, Enum
)
from sqlalchemy.orm import relationship
from ..database import Base

class MPGStatusEnum(str, enum.Enum):
    NOT_ISSUED         = "NOT Issued"
    ISSUED_EXTENDED    = "Issued / Extended"
    EXTENSION_REQUIRED = "Extension Required"
    NOT_RELEASED       = "NOT Released"
    RELEASED           = "Released"

class MaterialPerformanceGuarantee(Base):
    __tablename__ = "material_performance_guarantees"

    mpg_id                   = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id                 = Column(
        Integer,
        ForeignKey("order_details.order_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    mpg_no                   = Column(String(100), nullable=False, index=True)
    mpg_issuing_bank         = Column(String(100), nullable=True)
    mpg_deposit_receipt_no   = Column(String(100), nullable=True)
    cheque_no                = Column(String(50),  nullable=True)
    tt_date                  = Column(Date, nullable=True)
    document_date            = Column(Date, nullable=True)
    mpg_value                = Column(Numeric(12,2), nullable=False)
    mpg_expiry_date          = Column(Date, nullable=False)
    mpg_submitted_date       = Column(Date, nullable=True)
    mpg_return_date          = Column(Date, nullable=True)
    mpg_release_date_dewa    = Column(Date, nullable=True)
    mpg_release_date_bank    = Column(Date, nullable=True)
    mpg_extension_dates      = Column(ARRAY(Date), nullable=True)
    remarks                  = Column(Text, nullable=True)
    pending_status           = Column(
                                 Enum(MPGStatusEnum, name="mpg_status_enum"),
                                 nullable=False,
                                 default=MPGStatusEnum.NOT_ISSUED
                               )

    order                    = relationship("OrderDetail", back_populates="material_performance_guarantees")

    def __repr__(self) -> str:
        return (
            f"<MaterialPerformanceGuarantee(mpg_id={self.mpg_id!r}, "
            f"order_id={self.order_id!r}, mpg_no={self.mpg_no!r}, "
            f"pending_status={self.pending_status!r})>"
        )
