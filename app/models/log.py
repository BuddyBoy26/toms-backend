from sqlalchemy import Column, Integer, String, Date, Time, JSON, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, server_default=func.current_date(), nullable=False, index=True)
    time = Column(Time, server_default=func.current_time(), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    evidence = Column(JSON, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="logs")

    def __repr__(self) -> str:
        return (
            f"<Log(id={self.id!r}, date={self.date!r}, time={self.time!r}, "
            f"title={self.title!r}, user_id={self.user_id!r})>"
        )