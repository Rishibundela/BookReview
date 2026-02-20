from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class ReviewRead(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique identifier for the review")
    book_id: Optional[uuid.UUID] = Field(..., description="ID of the book being reviewed")
    user_id: Optional[uuid.UUID] = Field(..., description="ID of the user who wrote the review")
    rating: int = Field(..., ge=1, le=5, description="Rating for the book (1-5)")
    review_text: Optional[str] = Field(None, description="Optional review comment about the book")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="Timestamp when the review was created")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, description="Timestamp of the last update to the review")
    
class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating for the book (1-5)")
    review_text: Optional[str] = Field(None, description="Optional review comment about the book")