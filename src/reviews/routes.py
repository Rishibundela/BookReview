from fastapi import APIRouter, Depends, HTTPException, status
from src.reviews.service import ReviewService
from src.reviews.schemas import ReviewCreate, ReviewRead
from src.auth.dependencies import get_current_user
from src.db.models import User
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

review_router = APIRouter()
review_service = ReviewService()

@review_router.post("/book/{book_id}", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_review(
      book_id: str,
      review_data: ReviewCreate,
      current_user: User = Depends(get_current_user),
      session: AsyncSession = Depends(get_session)
    ):
    new_review = await review_service.create_review(
        user_email = current_user.email, 
        book_id=book_id, 
        review_data=review_data, 
        session=session
      )
    return new_review
