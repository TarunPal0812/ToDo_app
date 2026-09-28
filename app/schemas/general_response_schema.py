from pydantic import BaseModel
from typing import TypeVar, Any

T = TypeVar("T")

class SuccessResponse[T](BaseModel):
    success: bool = True
    message:str
    data: T | None = None
    meta: dict[str, Any] | None = None
