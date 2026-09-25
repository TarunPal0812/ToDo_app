"""
1. we will have to extract the token from the header
2. verify the token if valid then extract the claims
3. we will also have to check whether the user exis or not in the db
4. check for is_active
5. check for password changing **
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated, Any

from app.models.user import User
from app.repositories.user import UserRepository
from app.db.database import get_db

from app.security import verify_access_token

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

bearer = HTTPBearer()

async def get_current_user(
        crendentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
        db: Annotated[AsyncSession, Depends(get_db)]
    ):

    token = crendentials.credentials

    if token is None:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid token"
        )
    try:
        claims: dict[str, Any] = verify_access_token(token)

    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid token"
        )
    
    user_id = claims.get("sub")
    user = await UserRepository(db).get_user_by_id(UUID(user_id))

    # Check for user exist or not
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid token"
        )
    # Check if the user exist or not
    elif not user.is_active:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid token"
        )

    # Check for the password change
    """
    1. if we maintain a token version in our db and associate the version whith the tokne, and when a user change the password then we can increment the version of the token in the db

    2. after getting the token during the time of verification we can get the latest value of the token version and if it mismatch with the version what we get from token then we can unauthrorize the token
    """
    
    
    return user
   

securityDependency = Annotated[User,Depends(get_current_user)]