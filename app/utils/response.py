from app.schemas.general_response_schema import SuccessResponse
from typing import TypeVar, Any

T = TypeVar("T")

def success_response[T]( 
    data: T | None = None,
    *,
    message: str = "Success",
    meta: dict[str,Any] | None = None
) -> SuccessResponse:
    return SuccessResponse(success= True, message= message, data= data,meta= meta)