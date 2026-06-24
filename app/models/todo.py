from datetime import datetime
from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Todo(Base):
    __tablename__ = "todos"

    todo_id    = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content    = Column(Text, nullable=False)
    is_done    = Column(Boolean, nullable=False, default=False)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship("User", backref="todos")

    def __repr__(self) -> str:
        return f"<Todo(todo_id={self.todo_id!r}, done={self.is_done!r})>"