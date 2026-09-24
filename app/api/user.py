from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserResponse, UserCreate, UserLogin
from app.dependencies.user_dependencies import userServiceDependecy
from app.dependencies.secutiry_dependencies import securityDependency


router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/register",response_model= UserResponse)
async def register_user(user_service: userServiceDependecy, user_in: UserCreate):
    created_user = await user_service.register(user_in)
    if created_user is None:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "unable to create user"
        )
    else:
        return created_user

@router.post("/login")
async def login_user(user_service: userServiceDependecy, user_in: UserLogin):
    return await user_service.login(user_in)

@router.get("/me", response_model= UserResponse)
async def get_me(current_user: securityDependency):
    return current_user