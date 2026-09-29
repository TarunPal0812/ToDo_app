from datetime import datetime
from uuid import UUID

from typing  import Literal

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

class TodoListParams(BaseModel):
    is_completed: bool | None = None
    sort_by: Literal["created_at","name"] = "created_at"
    sort_order:Literal["asc","desc"] = "asc"

    limit: int = Field(default=10, ge=1, le=100)
    page: int = Field(default=1, ge=1)