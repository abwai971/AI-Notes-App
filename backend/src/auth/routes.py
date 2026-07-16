from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from .schemas import UserResponse, UserCreateModel, UserLoginModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService
from .dependencies import AccessTokenBearer, RefreshTokenBearer, get_current_user
from src.core.utils import verify_password, create_access_token
from datetime import timedelta,datetime

auth_router = APIRouter()
user_service = UserService()

#new user sign in
@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exists(email,session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")

    new_user = await user_service.create_user(user_data,session)

    return new_user

#logout
@auth_router.post("/logout")
async def logout_user(_: dict = Depends(AccessTokenBearer())):
    return {
        "message": "Logged out successfully"
    }

REFRESH_TOKEN_EXPIRY = 2
#user login
@auth_router.post("/login")
async def login_users(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):

    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data = {
                    'email': user.email,
                    'user_uid': str(user.uid),
                    'user_role': user.role
                }
            )
            refresh_token = create_access_token(
                user_data = {
                    'email': user.email,
                    'user_uid': str(user.uid)
                },
                expiry = timedelta(days=REFRESH_TOKEN_EXPIRY),
                refresh = True
            )

            return JSONResponse(
                content = {
                    "message": 'Login successful',
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        'user_email': user.email,
                        'user_uid': str(user.uid)
                    }
                }
            )
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")

#refresh token
@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
   
   expiry_timestamp = token_details['exp']
   if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
       
       new_access_token = create_access_token(
           user_data = token_details['user']
       )
       return JSONResponse(
           content = {
               "access_token": new_access_token
           }
       )
   raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired Token")

@auth_router.get("/me", response_model=UserResponse)
async def get_user(user = Depends(get_current_user)):
    return user
