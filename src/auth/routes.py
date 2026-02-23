from fastapi import APIRouter, Depends, HTTPException, status
from .schema import UserCreate, UserRead, UserLogin, UserReadWithBooks
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token, decode_access_token,verify_password
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from .dependencies import AccessTokenBearer, RefreshTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_token_to_blocklist, is_token_blocked 
from src.errors import InvalidCredentials, UserAlreadyExists, InvalidToken

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(allowed_roles=["admin","user"])  # Example role checker for admin-only routes

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    if await user_service.user_exists(user_data.email, session):
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)
    return new_user

@auth_router.get("/me", response_model=UserReadWithBooks, status_code=status.HTTP_200_OK)
async def read_current_user(current_user: dict = Depends(get_current_user), _:bool = Depends(role_checker)):
    if not current_user:
        raise InvalidCredentials()
    return current_user
  
@auth_router.post("/login")
async def login_user(login_data: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_email(login_data.email, session)

    if user is not None:
        password_valid = verify_password(login_data.password, user.password_hash) 

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "id": str(user.id), 
                    "email": user.email,
                    "role": user.role
                }
            )
            
            refresh_token = create_access_token(
                user_data={
                    "id": str(user.id), 
                    "email": user.email
                },
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
                refresh=True
            )
            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token, 
                    "refresh_token": refresh_token,
                    "user": {
                        "id": str(user.id),
                        "email": user.email
                    }
                }
            )

    raise InvalidCredentials()

@auth_router.post("/refresh_token")
async def new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details.get("exp")
    if datetime.fromtimestamp(expiry_timestamp) < datetime.now():
        raise InvalidToken()
    new_access_token = create_access_token(user_data=token_details["user"])

    return JSONResponse(
        content={
            "message": "Access token refreshed successfully",
            "access_token": new_access_token
        }
    )

@auth_router.post("/logout")
async def logout_user(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details.get("jti")
    if jti:
        await add_token_to_blocklist(jti)
        return JSONResponse(content={"message": "Logout successful"})
    
    raise InvalidToken()