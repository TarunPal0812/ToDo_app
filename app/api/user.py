from fastapi import APIRouter, HTTPException, status, Response
from app.schemas.user import UserResponse, UserCreate, UserLogin
from app.schemas.general_response_schema import SuccessResponse
from app.dependencies.user_dependencies import userServiceDependecy
from app.dependencies.secutiry_dependencies import securityDependency
from app.utils.response import success_response


router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/register",response_model= SuccessResponse[UserResponse])
async def register_user(user_service: userServiceDependecy, user_in: UserCreate):
    created_user = await user_service.register(user_in)
    if created_user is None:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "unable to create user"
        )
    else:
        return success_response(data=created_user, message= "User registerd successfully")

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

@router.get("/me", response_model= SuccessResponse[UserResponse])
async def get_me(current_user: securityDependency):
    return success_response(data=current_user, message="Getting the user successfully")