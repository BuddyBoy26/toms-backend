from sqlalchemy import Column, Integer, String, Text, DateTime
from ..database import Base
import datetime

class Event(Base):
    __tablename__ = "events"

    event_id      = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description   = Column(String(500), nullable=False, index=True)
    start_dt      = Column(DateTime, nullable=False, index=True)
    end_dt        = Column(DateTime, nullable=False, index=True)
    remarks       = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<Event(id={self.event_id!r}, desc={self.description!r}, "
            f"start={self.start_dt!r}, end={self.end_dt!r})>"
        )
