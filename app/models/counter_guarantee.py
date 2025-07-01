import enum
from sqlalchemy import (
    Column, Integer, Enum, Date, String, Text
)
from ..database import Base

class GuaranteeTypeEnum(str, enum.Enum):
    TBG = "TBG"
    PBG = "PBG"
    MPG = "MPG"

class PendingStatusEnum(str, enum.Enum):
    NOT_ISSUED         = "NOT Issued"
    ISSUED_EXTENDED    = "Issued / Extended"
    EXTENSION_REQUIRED = "Extension Required"
    NOT_RELEASED       = "NOT Released"
    RELEASED           = "Released"

class CounterGuarantee(Base):
    __tablename__ = "counter_guarantees"

    cg_id                = Column(Integer, primary_key=True, index=True, autoincrement=True)
    guarantee_type       = Column(Enum(GuaranteeTypeEnum, name="guarantee_type_enum"), nullable=False)
    guarantee_ref_number = Column(String(100), nullable=False, index=True)  # was ref_id
    cg_date              = Column(Date, nullable=False)
    issuing_bank         = Column(String(100), nullable=True)
    expiry_date          = Column(Date, nullable=False)
    release_date_bank    = Column(Date, nullable=True)
    remarks              = Column(Text, nullable=True)
    pending_status       = Column(Enum(PendingStatusEnum, name="cg_pending_status_enum"),
                                  nullable=False, default=PendingStatusEnum.NOT_ISSUED)

    def __repr__(self) -> str:
        return (
            f"<CounterGuarantee(cg_id={self.cg_id!r}, "
            f"type={self.guarantee_type!r}, "
            f"ref_number={self.guarantee_ref_number!r})>"
        )
