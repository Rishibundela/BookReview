import hashlib
from pickle import load
from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config import Config
import uuid
import jwt
import logging

ACCESS_TOKEN_EXPIRY = 3600  

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    sha_hash = hashlib.sha256(password_bytes).hexdigest()
    return password_context.hash(sha_hash)


def verify_password(password: str, hashed: str) -> bool:
    password_bytes = password.encode("utf-8")
    sha_hash = hashlib.sha256(password_bytes).hexdigest()
    return password_context.verify(sha_hash, hashed)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool= False) :
      
    payload = {}

    payload ["user" ] = user_data
    payload ["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )

    payload [ 'jti' ] = str(uuid.uuid4())

    payload [ 'refresh' ] = refresh

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )

    return token

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
        return payload
    except jwt.PyJWTError as e:
        logging.error(f"Token decoding error: {e}")
        return None