from pwdlib import PasswordHash
import jwt
from uuid import UUID
from app.config.config import setting
from datetime import datetime, timezone, timedelta
from typing import Any

password_context = PasswordHash.recommended()

def hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def generate_token(user_id: UUID):
    now = datetime.now(tz= timezone.utc)
    payload: dict[str,Any] = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(seconds= 60 * 15)
    }
    return jwt.encode(payload,setting.JWT_SECRET,algorithm="HS256")

def verify_token(token: str):
    return jwt.decode(token,setting.JWT_SECRET, algorithms=["HS256"])

