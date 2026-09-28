from fastapi import status, Request, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .exceptions import AppError, UserAlreadyExist
from .responses import ErrorDetails, ErrorResponse

ERROR_STATUS_CODE: dict[type[AppError], int] = {
    UserAlreadyExist: status.HTTP_409_CONFLICT
}


async def app_error_handeler(request: Request, exec: AppError) -> JSONResponse:
    status_code = ERROR_STATUS_CODE.get(
        type(exec),
        status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    response = ErrorResponse(
        error= ErrorDetails(
            code= exec.code,
            message= exec.message,
            details= exec.details  
        )
    )
    return JSONResponse(
        status_code= status_code,
        content= response.model_dump(mode='json')
    )

async def unexpected_error_handler(request: Request, exc: Exception):

    response = ErrorResponse(
        error=ErrorDetails(code="INTERNAL_SERVER_ERROR", message="Internal server error")
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(mode="json"),
    )


async def validation_error_handeler(request: Request, exec: RequestValidationError):
    validation_error = []

    for error in exec.errors():
        validation_error.append(
            {
                "location": list(error["loc"]),
                "message": error["msg"],
                "type": error["type"]

            }
        )
    response = ErrorResponse(
            error= ErrorDetails(
                code= "VALIDATION_ERROR",
                message= "validation fail",
                details= validation_error
            )
        )

    return JSONResponse(
            status_code= status.HTTP_422_UNPROCESSABLE_CONTENT,
            content= response.model_dump(mode="json")
        )


def register_exceptions_handelers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handeler)  # type: ignore
    app.add_exception_handler(RequestValidationError, validation_error_handeler) # type: ignore
    app.add_exception_handler(Exception, unexpected_error_handler)
