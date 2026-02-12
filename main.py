from fastapi import FastAPI, Header, Query, Path, status
from fastapi.exceptions import HTTPException
from typing import Optional,List
from pydantic import BaseModel
import uuid

app = FastAPI()

books = [
  {
    "id": 1,
    "title": "Think Python",
    "author": "Allen B. Downey",
    "publisher": "0'Reilly Media",
    "published_date": "2021-01-01",
    "page_count": 1234,
    "language": "English"
  },
  {
    "id": 2,
    "title": "Python Crash Course", 
    "author": "Eric Matthes", 
    "publisher": "No Starch Press", 
    "published_date": "2019-01-01", 
    "page_count": 567, 
    "language": "English"
  },
  {
    "id": 3, 
    "title": "Automate the Boring Stuff with Python",
    "author": "Al Sweigart", 
    "publisher": "No Starch Press",
    "published_date": "2015-01-01", 
    "page_count": 789, 
    "language":"English"
  },
  {
    "id": 4, 
    "title": "Python for Data Analysis", 
    "author": "Wes McKinney", 
    "publisher": "O'Reilly Media", 
    "published_date": "2017-01-01", 
    "page_count": 987, 
    "language": "English"
  },
  {
    "id": 5, 
    "title": "Fluent Python", 
    "author": "Luciano Ramalho", 
    "publisher": "O'Reilly Media", 
    "published_date": "2016-01-01", 
    "page_count": 654, 
    "language": "English"
  }
]

class Book(BaseModel):
  id: Optional[int] = None
  title: str
  author: str
  publisher: str
  published_date: str
  page_count: int
  language: str

class BookUpdate(BaseModel):
  title: Optional[str] = None
  author: Optional[str] = None
  publisher: Optional[str] = None
  published_date: Optional[str] = None
  page_count: Optional[int] = None
  language: Optional[str] = None

@app.get("/books", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books() -> List[Book]:
    # Return all books
    return books

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: Book) -> Book:
  
  new_book = book.model_dump()
  books.append(new_book)
  return new_book

@app.get("/books/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Path(..., gt=0, description="The ID of the book to retrieve",example=1)) -> Book:

  for book in books:
    if book["id"] == book_id:
      return book
    
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.patch("/books/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(
  book_id: int = Path(..., gt=0, description="The ID of the book to update",example=1),
  book_update_data: BookUpdate = None
  ) -> Book:

  for i, b in enumerate(books):
    if b["id"] == book_id:
      updated_book = {**b, **book_update_data.model_dump(exclude_unset=True)}
      books[i] = updated_book
      return updated_book
    
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(..., gt=0, description="The ID of the book to delete",example=1)):

  for book in books:
    if book["id"] == book_id:
      books.remove(book)
      return
    
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")