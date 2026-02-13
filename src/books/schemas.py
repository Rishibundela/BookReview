from typing import Optional,List
from pydantic import BaseModel
from datetime import datetime, date
import uuid
class Book(BaseModel):
  id: uuid.UUID
  title: str
  author: str
  publisher: str
  published_date: date
  page_count: int
  language: str
  created_at: datetime
  updated_at: datetime


class BookCreate(BaseModel):
  title: str
  author: str
  publisher: str
  published_date: date
  page_count: int
  language: str

class BookUpdate(BaseModel):
  title: Optional[str] = None
  author: Optional[str] = None
  publisher: Optional[str] = None
  published_date: Optional[date] = None
  page_count: Optional[int] = None
  language: Optional[str] = None