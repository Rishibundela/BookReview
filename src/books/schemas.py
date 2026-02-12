from typing import Optional,List
from pydantic import BaseModel
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