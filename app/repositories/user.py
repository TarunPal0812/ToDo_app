from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select

class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self.db.get(User, user_id)

    async def get_user_by_email(self, user_email: str) -> User | None:
        user = await self.db.execute(select(User).where(User.email == user_email))
        return user.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

