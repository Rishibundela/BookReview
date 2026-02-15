from fastapi import APIRouter, Path, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.books.service import BookService
from fastapi.exceptions import HTTPException
from typing import List
from src.books.schemas import Book, BookUpdate, BookCreate
from src.auth.dependencies import AccessTokenBearer


book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()  # Initialize the access token bearer

@book_router.get("/", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books(
    session: AsyncSession = Depends(get_session), 
    user_details = Depends(access_token_bearer)) -> List[Book]:
    
    print("User details from token:", user_details)  # Debugging line to check token data
    books = await book_service.get_all_books(session)
    return books

@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(
  book: BookCreate, 
  session: AsyncSession = Depends(get_session),
  user_details = Depends(access_token_bearer)) -> Book:

  new_book = await book_service.create_book(book, session)
  return new_book

@book_router.get("/{book_uid}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(
  book_uid: str = Path(..., description="The ID of the book to retrieve"), 
  session: AsyncSession = Depends(get_session),
  user_details = Depends(access_token_bearer)) -> Book:

  book = await book_service.get_book(book_uid, session)
  if not book:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
  return book

@book_router.patch("/{book_uid}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(
  book_update_data: BookUpdate,
  book_uid: str = Path(..., description="The ID of the book to update"),
  session: AsyncSession = Depends(get_session),
  user_details = Depends(access_token_bearer)) -> Book:

  updated_book = await book_service.update_book(book_uid, book_update_data, session)
  if not updated_book:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
  return updated_book

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
  book_uid: str = Path(..., description="The ID of the book to delete"), 
  session: AsyncSession = Depends(get_session),
  user_details = Depends(access_token_bearer)):

  deleted_book = await book_service.delete_book(book_uid, session)
  if not deleted_book:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
  return {"detail": "Book deleted successfully"}