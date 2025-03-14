from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    uid: str


class UserUpdate(UserBase):
    pass


class UserResponse(UserBase):
    id: UUID
    uid: str
