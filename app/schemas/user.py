from pydantic import BaseModel, EmailStr
from fastapi import Depends, HTTPException, status
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    password: str                                  # <— plain-text password from client

class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str                                  # <— plain-text password from client