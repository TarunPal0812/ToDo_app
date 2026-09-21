from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TodoBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    is_completed: bool = False


class TodoCreate(TodoBase):
   pass


class TodoUpdate(BaseModel):   
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    is_completed: bool | None = None


class TodoResponse(TodoBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )