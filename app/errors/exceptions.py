from typing import Any

class AppError(Exception):
    code = "APP_ERROR"
    message = "an application error occurred"

    def __init__(self, details: dict[str,Any] | None = None) -> None:
        self.details = details
        super().__init__(self.message)

class UserAlreadyExist(AppError):
    code = "USER_ALREADY_EXIST"
    message = "user already exist"

class TodoAlreadyExist(AppError):
    code = "TODO_ALREADY_EXIST"
    message = "todo with the same name already exist"

class UserUnableToCreate(AppError):
    code = "USER_UNABLE_TO_CREATE"
    message = "user unable to create"

class InvalidCredentials(AppError):
    code = "INVALID_CREDENTIALS"
    message = "invalid credentials"

class InvalidToken(AppError):
    code = "INVALID_TOKEN"
    message = "invalid token"

class UnauthorizedAccess(AppError):
    code = "UNAUTHORIZED_ACCESS"
    message = "unauthorized access"

class TodoNotFound(AppError):
    code = "TODO_NOT_FOUND"
    message = "todo not found"