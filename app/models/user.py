from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    logs = relationship("Log", back_populates="user")

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id!r}, email={self.email!r}, "
            f"full_name={self.full_name!r}, created_at={self.created_at!r})>"
        )



