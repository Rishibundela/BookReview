from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreate, BookUpdate
from .models import Book
from sqlmodel import select
from datetime import datetime

class BookService:
  async def get_all_books(self, session: AsyncSession):
    statement = select(Book).order_by(Book.created_at.desc())
    result = await session.exec(statement)
    return result.all()  # always returns a list, even if it's empty
  
  async def create_book(self, book_data: BookCreate, session: AsyncSession):
    new_book = Book(**book_data.model_dump())

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)

    return new_book
  
  async def get_book(self, book_id:str, session: AsyncSession):
    statement = select(Book).where(Book.id == book_id)
    result = await session.exec(statement)
    return result.first()   # Returns the first matching book or None if not found
  
  async def update_book(self, book_id:str, book_data: BookUpdate, session: AsyncSession):
    book = await self.get_book(book_id, session)

    if not book:
        return None

    update_dict = book_data.model_dump(exclude_unset=True)

    for field, value in update_dict.items():
        setattr(book, field, value)

    await session.commit()
    await session.refresh(book)

    return book

  async def delete_book(self, book_id:str, session: AsyncSession):
    book = await self.get_book(book_id, session)

    if not book:
        return None

    await session.delete(book)
    await session.commit()

    return book  # Optionally return the deleted book's data for confirmation

    # fetch row -> modify -> commit -> refresh -> return modified row