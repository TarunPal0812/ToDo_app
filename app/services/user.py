from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from fastapi import HTTPException, status
from app.security import hashed_password, verify_password

class UserService:
    def __init__(self, repo:UserRepository) -> None:
        self.repo = repo

    async def register(self, user_in: UserCreate):
        existing_user = await self.repo.get_user_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email alrady exist"
            )
        password_hash: str = hashed_password(user_in.password)

        user_object = User(
            email = user_in.email,
            hash_password = password_hash
        )

        created_user = await self.repo.create(user_object)

        if not created_user:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="User unable to create"
            )
        return created_user
        

    async def login(self, user_crendential:UserLogin):
        existing_user = await self.repo.get_user_by_email(user_crendential.email)
        if not existing_user:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Invalid crendential"
            )
        is_verify = verify_password(user_crendential.password, existing_user.hash_password)

        if not is_verify:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="invalid crendential"
            )
        return {
            "msg" : "Login sussessfull..!!"
        }
    