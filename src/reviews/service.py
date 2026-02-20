from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from .schemas import ReviewCreate
import logging

user_service = UserService()
book_service = BookService()

class ReviewService:

    async def create_review(
        self, user_email: str, book_id: str, review_data: ReviewCreate, session: AsyncSession):

        try:
            user = await user_service.get_user_by_email(user_email, session)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            book = await book_service.get_book(book_id, session)
            if not book:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

            review = Review(
                user_id=user.id,
                book_id=book.id,
                **review_data.model_dump()
            )
            session.add(review)
            await session.commit()
            await session.refresh(review)
            return review
        except Exception as e:
            logging.error(f"Error creating review: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="OOPS! Something went wrong while creating the review. Please try again.")