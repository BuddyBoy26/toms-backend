from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


def get_todos_by_user(db: Session, user_id: int) -> List[Todo]:
    return (
        db.query(Todo)
        .filter(Todo.user_id == user_id)
        .order_by(Todo.created_at.asc())
        .all()
    )


def create_todo(db: Session, t: TodoCreate, user_id: int) -> Todo:
    obj = Todo(content=t.content, user_id=user_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def toggle_todo(db: Session, todo_id: int, user_id: int, t: TodoUpdate) -> Optional[Todo]:
    obj = db.query(Todo).filter(Todo.todo_id == todo_id, Todo.user_id == user_id).first()
    if not obj:
        return None
    obj.is_done = t.is_done
    db.commit()
    db.refresh(obj)
    return obj


def delete_todo(db: Session, todo_id: int, user_id: int) -> Optional[Todo]:
    obj = db.query(Todo).filter(Todo.todo_id == todo_id, Todo.user_id == user_id).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj