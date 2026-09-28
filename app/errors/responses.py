from pydantic import BaseModel
from typing import Any

class ErrorDetails(BaseModel):
    code: str
    message: str
    details: Any | None = None

class ErrorResponse(BaseModel):
    error: ErrorDetails