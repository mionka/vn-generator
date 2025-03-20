from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    uid: str


class UserUpdate(UserBase):
    dt_updated: datetime


class UserResponse(UserBase):
    id: UUID
    uid: str
