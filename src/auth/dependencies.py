from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Request
from .utils import decode_access_token
from src.db.redis import is_token_blocked
from fastapi import Depends
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from typing import List, Any

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials = await super().__call__(request)
        
        token = credentials.credentials if credentials else None
        token_data = decode_access_token(token) if token else None

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Invalid or expired access token. Please log in again."
            )
        
        if token_data and await is_token_blocked(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="This token has been revoked. Please log in again."
            )
        
        self.verify_token_data(token_data)
        
        return token_data if token_data else None
        
    
    def token_valid(self, token: str) -> bool:
        # Implement your token validation logic here
        # For example, you can decode the token and check its validity
        token_data = decode_access_token(token)
        
        return token_data is not None
    
    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Subclasses must implement this method to verify token data")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        # Implement your access token specific validation logic here
        # For example, you can check if the token has the correct scopes or permissions
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Please provide a valid access token, refresh tokens are not allowed"
            )

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        # Implement your refresh token specific validation logic here
        # For example, you can check if the token has the correct scopes or permissions
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Please provide a valid refresh token, access tokens are not allowed"
            ) 
        
async def get_current_user(
        token_data: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session)) -> dict:
    # This function can be used in your routes to get the current user's details from the token
    user_email = token_data['user']['email']
    user = await user_service.get_user_by_email(user_email, session)

    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: dict = Depends(get_current_user)) -> Any:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="You do not have permission to perform this action."
            )
        return True
