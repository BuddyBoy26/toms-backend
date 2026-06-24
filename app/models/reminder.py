import enum
from datetime import date, datetime
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Boolean, Text,
    ForeignKey, Enum, UniqueConstraint
)
from sqlalchemy.orm import relationship
from ..database import Base


class ReminderTypeEnum(str, enum.Enum):
    # ── Immediate (activation_date = day the trigger field is saved) ──
    TBG_TO_BE_ISSUED         = "TBG_TO_BE_ISSUED"
    PBG_TO_BE_ISSUED         = "PBG_TO_BE_ISSUED"
    TBG_TO_BE_RELEASED       = "TBG_TO_BE_RELEASED"
    MPG_TO_BE_ISSUED         = "MPG_TO_BE_ISSUED"
    PBG_TO_BE_RELEASED       = "PBG_TO_BE_RELEASED"
    GET_ETD                  = "GET_ETD"
    GET_CUSTOMS_EXEMPTION    = "GET_CUSTOMS_EXEMPTION"
    PREPARE_ASN              = "PREPARE_ASN"
    CREATE_DELIVERY_NOTE     = "CREATE_DELIVERY_NOTE"
    PAYMENT_APPLICATION      = "PAYMENT_APPLICATION"
    PREPARE_LD_STATEMENT     = "PREPARE_LD_STATEMENT"

    # ── Date-based (activation_date = the calculated future / target date) ──
    MPG_TO_BE_RELEASED       = "MPG_TO_BE_RELEASED"
    INSPECTION_APPLICATION   = "INSPECTION_APPLICATION"
    GET_SHIPPING_DOCUMENTS   = "GET_SHIPPING_DOCUMENTS"


class Reminder(Base):
    __tablename__ = "reminders"

    reminder_id    = Column(Integer, primary_key=True, index=True, autoincrement=True)

    reminder_type  = Column(
        Enum(ReminderTypeEnum, name="reminder_type_enum"),
        nullable=False,
        index=True,
    )

    # Nullable FK — tender-level reminders may not have an order yet
    order_id       = Column(
        Integer,
        ForeignKey("order_details.order_id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    po_number      = Column(String(200), nullable=False)
    description    = Column(Text, nullable=False)
    activation_date = Column(Date, nullable=False, index=True)

    is_dismissed   = Column(Boolean, nullable=False, default=False, index=True)

    # Which table + row triggered this reminder (for dedup / cleanup)
    source_table   = Column(String(100), nullable=False)
    source_id      = Column(Integer, nullable=False)

    created_at     = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at     = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ── Unique constraint: one reminder per (type, source_table, source_id) ──
    __table_args__ = (
        UniqueConstraint(
            "reminder_type", "source_table", "source_id",
            name="uq_reminder_type_source"
        ),
    )

    order = relationship("OrderDetail", backref="reminders")

    def __repr__(self) -> str:
        return (
            f"<Reminder(reminder_id={self.reminder_id!r}, "
            f"type={self.reminder_type!r}, po={self.po_number!r}, "
            f"active={self.activation_date!r})>"
        )