from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=5, max_length=10)



class UserCreate(UserBase):
   pass


class UserLogin(UserBase):
    pass


class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )