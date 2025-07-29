from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional, Any, Dict

class LogBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    evidence: Optional[Dict[str, Any]] = None

class LogCreate(LogBase):
    """title + description required; evidence optional"""

class LogRead(LogBase):
    id: int
    date: date
    time: time
    user_id: int

    class Config:
        from_attributes = True
