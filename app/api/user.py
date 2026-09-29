from fastapi import APIRouter, status, Response
from app.schemas.user import UserResponse, UserCreate, UserLogin
from app.schemas.general_response_schema import SuccessResponse
from app.dependencies.user_dependencies import userServiceDependecy
from app.dependencies.secutiry_dependencies import securityDependency
from app.utils.response import success_response
from app.errors.exceptions import UserUnableToCreate


router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/register",response_model= SuccessResponse[UserResponse])
async def register_user(user_service: userServiceDependecy, user_in: UserCreate):
    created_user = await user_service.register(user_in)
    if created_user is None:
        raise UserUnableToCreate()
    else:
        return success_response(
            # data=created_user,
            message= "User registerd successfully"
        )

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
    return success_response(data= access_token, message="Login successfull")

@router.get("/me", response_model= SuccessResponse[UserResponse])
async def get_me(current_user: securityDependency):
    return success_response(data=current_user, message="Getting the user successfully")