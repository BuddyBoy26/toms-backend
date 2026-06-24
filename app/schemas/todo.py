from pydantic import BaseModel
from datetime import datetime


class TodoCreate(BaseModel):
    content: str


class TodoUpdate(BaseModel):
    is_done: bool


class TodoRead(BaseModel):
    todo_id: int
    content: str
    is_done: bool
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True