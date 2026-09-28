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