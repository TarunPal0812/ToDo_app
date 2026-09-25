from fastapi import APIRouter, Request, HTTPException, status, Depends, Response
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.security import verify_refresh_token
from app.repositories.user import UserRepository
from app.db.database import get_db
from uuid import UUID
from app.security import generate_access_token, generate_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/refresh-access-token")
async def refresh_access_token(
    request: Request,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    refresh_token = request.cookies.get("refresh-token")
    if not refresh_token:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access"
        )
    try:
        claims = verify_refresh_token(refresh_token)
    except:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access"
        )
    
    userId = claims["sub"]

    user = await UserRepository(db).get_user_by_id(UUID(userId))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access",
        )

    # Check the password change for refresh the token

    access_token = generate_access_token(user.id)
    new_refresh_token = generate_refresh_token(user.id)

    response.set_cookie(
        "refresh-token",
        new_refresh_token,
        max_age= 24 * 3600,
        # secure= True,
        samesite= "lax"
    )

    return {
        "token": access_token
    }

