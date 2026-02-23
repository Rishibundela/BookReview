from fastapi import APIRouter, Depends, HTTPException, status
from .schema import UserCreate, UserRead, UserLogin, UserReadWithBooks, EmailModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token, verify_password, create_url_safe_token, decode_url_safe_token
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from .dependencies import AccessTokenBearer, RefreshTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_token_to_blocklist, is_token_blocked 
from src.errors import InvalidCredentials, UserAlreadyExists, InvalidToken, UserNotFound
from src.mail import create_message, mail
from src.config import Config

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(allowed_roles=["admin","user"])  # Example role checker for admin-only routes

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post("/send_mail")
async def send_mail(emails: EmailModel):

    emails = emails.addresses

    html = "<h1> Welcome to the app </h1>"

    message = create_message(
        recipients=emails,
        subject="Welcome", 
        body=html
    )

    await mail.send_message(message)
    return {"message": "Email sent successfully"}

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    email= user_data.email
    if await user_service.user_exists(email, session):
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
    <h1>Verify your Email</h1>
    <p>Please click this <a href="{link}">link</a> to verify your email</p>
    """

    message = create_message(
        recipients=[email], subject="Verify your email", body=html_message
    )

    await mail.send_message(message)

    return {
        "message": "Account Created! Check email to verify your account",
        "user": new_user,
    }

@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

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