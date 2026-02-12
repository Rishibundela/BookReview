from fastapi import APIRouter
from fastapi import FastAPI, Header, Query, Path, status
from fastapi.exceptions import HTTPException
from typing import List
from src.books.schemas import Book, BookUpdate
from src.books.book_data import books


book_router = APIRouter()

@book_router.get("/", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books() -> List[Book]:
    # Return all books
    return books

@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: Book) -> Book:
  
  new_book = book.model_dump()
  books.append(new_book)
  return new_book

@book_router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Path(..., gt=0, description="The ID of the book to retrieve",examples=1)) -> Book:

  for book in books:
    if book["id"] == book_id:
      return book
    
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.patch("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(
  book_update_data: BookUpdate,
  book_id: int = Path(..., gt=0, description="The ID of the book to update",examples=1)
  ) -> Book:

  for i, b in enumerate(books):
    if b["id"] == book_id:
      updated_book = {**b, **book_update_data.model_dump(exclude_unset=True)}
      books[i] = updated_book
      return updated_book
    
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(..., gt=0, description="The ID of the book to delete",examples=1)):

  for book in books:
    if book["id"] == book_id:
      books.remove(book)
      return
    
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")