from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    nickname: str

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    nickname: Optional[str] = None

class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True 