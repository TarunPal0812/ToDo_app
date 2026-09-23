from fastapi import Depends
from typing import Annotated
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

def get_user_service(db_session: Annotated[AsyncSession, Depends(get_db)]):
    repo = UserRepository(db= db_session)
    return UserService(repo)

userServiceDependecy = Annotated[UserService,Depends(get_user_service)]


