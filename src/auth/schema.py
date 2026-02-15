from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    first_name: str = Field(..., max_length=30, example="John")
    last_name: str = Field(..., max_length=30, example="Doe")
    username: str = Field(..., max_length=8, example="john_doe")
    email: str = Field(..., max_length=40, example="john.doe@example.com")
    password: str = Field(..., min_length=6, max_length=20, example="P@ssw0rd")

class UserRead(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime  

class UserLogin(BaseModel):
    email: str = Field(..., max_length=40, example="john.doe@example.com")
    password: str = Field(..., min_length=6, max_length=20, example="P@ssw0rd")
    