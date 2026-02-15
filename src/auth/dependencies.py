from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Request
from .utils import decode_access_token
from src.db.redis import is_token_blocked

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
    
    def verify_token_data(self, token_data: dict) -> bool:
        raise NotImplementedError("Subclasses must implement this method to verify token data")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> bool:
        # Implement your access token specific validation logic here
        # For example, you can check if the token has the correct scopes or permissions
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Please provide a valid access token, refresh tokens are not allowed"
            )

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> bool:
        # Implement your refresh token specific validation logic here
        # For example, you can check if the token has the correct scopes or permissions
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Please provide a valid refresh token, access tokens are not allowed"
            ) 