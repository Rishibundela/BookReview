from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import RoleChecker, get_current_user
from src.db.main import get_session
from src.db.models import User

from .schemas import ReviewCreate, ReviewRead
from .service import ReviewService
from src.errors import ReviewNotFound

review_service = ReviewService()
review_router = APIRouter()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["user", "admin"]))

@review_router.get("/", response_model=list[ReviewRead], status_code=status.HTTP_200_OK, dependencies=[admin_role_checker])
async def get_all_reviews(session: AsyncSession = Depends(get_session)) -> list[ReviewRead]:
  reviews = await review_service.get_all_reviews(session)
  return reviews

@review_router.get("/{review_id}", response_model=ReviewRead, status_code=status.HTTP_200_OK, dependencies=[user_role_checker])
async def get_review(review_id: str, session: AsyncSession = Depends(get_session)) -> ReviewRead:
  review = await review_service.get_review(review_id, session)
  if not review:
    raise ReviewNotFound()
  return review

@review_router.post("/book/{book_id}", response_model=ReviewRead, status_code=status.HTTP_201_CREATED, dependencies=[user_role_checker])
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

@review_router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[user_role_checker])
async def delete_review(
  review_id: str,
  current_user: User = Depends(get_current_user), 
  session: AsyncSession = Depends(get_session)):
  deleted_review = await review_service.delete_review(review_id, current_user.email, session)
  if not deleted_review:
    raise ReviewNotFound()
  return {"detail": "Review deleted successfully"}
