from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import app.cruds.todo as cruds
import app.schemas.todo as schemas
from ..database import get_db
from ..routers.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["todos"])


@router.get("/", response_model=List[schemas.TodoRead])
def list_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cruds.get_todos_by_user(db, current_user.id)


@router.post("/", response_model=schemas.TodoRead, status_code=201)
def create_todo(
    t: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not t.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    return cruds.create_todo(db, t, current_user.id)


@router.patch("/{todo_id}", response_model=schemas.TodoRead)
def toggle_todo(
    todo_id: int,
    t: schemas.TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.toggle_todo(db, todo_id, current_user.id, t)
    if not obj:
        raise HTTPException(status_code=404, detail="Todo not found")
    return obj


@router.delete("/{todo_id}", response_model=schemas.TodoRead)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = cruds.delete_todo(db, todo_id, current_user.id)
    if not obj:
        raise HTTPException(status_code=404, detail="Todo not found")
    return obj