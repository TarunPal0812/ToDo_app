from fastapi import APIRouter, HTTPException, status, Response
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
async def login_user(user_service: userServiceDependecy, user_in: UserLogin, response: Response):
    tokens = await user_service.login(user_in)
    access_token = tokens["token"]
    refresh_token = tokens["refresh_token"]
  
    response.set_cookie(
        "refresh-token",
        refresh_token,
        max_age= 24 * 3600,
        # secure= True,
        samesite= "lax"
    )
    return {
        "token": access_token
    }

@router.get("/me", response_model= UserResponse)
async def get_me(current_user: securityDependency):
    return current_user