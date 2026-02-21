from sqlmodel import SQLModel, Field, Column, Relationship, ForeignKey
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import func
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(
          sa_column=Column(
            pg.UUID, 
            nullable=False,  
            primary_key=True,
            default=uuid.uuid4
          )
      )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    password_hash: str = Field(exclude=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False))
    books: List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"} )
    reviews: List["Review"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"} )
    
    def __repr__(self):
      return f"<User {self.username}>"
    
class BookTag(SQLModel, table=True):
    __tablename__ = "book_tag"

    book_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            ForeignKey("books.id"),
            primary_key=True
        )
    )

    tag_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            ForeignKey("tags.id"),
            primary_key=True
        )
    )

class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(
        sa_column=Column(
           pg.UUID, 
           nullable=False,  
           primary_key=True,
          default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False))
    user: Optional[User] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy": "selectin"} )
    tags: List["Tag"] = Relationship(link_model=BookTag, back_populates="books")

    def __repr__(self):
      return f"<Book {self.title} by {self.author}>"
    
class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: uuid.UUID = Field(
        sa_column=Column(
           pg.UUID, 
           nullable=False,  
           primary_key=True,
          default=uuid.uuid4
        )
    )
    book_id: Optional[uuid.UUID] = Field(default=None, foreign_key="books.id")
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    rating: int = Field(lt=5, gt=0)
    review_text: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False))
    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[Book] = Relationship(back_populates="reviews")

    def __repr__(self):
      return f"<Review {self.rating} stars by {self.user_id} for book_id {self.book_id}>"
    

class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            nullable=False
        )
    )

    name: str = Field(
        sa_column=Column(
            pg.VARCHAR,
            nullable=False,
            unique=True,
            index=True
        )
    )

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now()
        )
    )

    books: List["Book"] = Relationship(
        link_model=BookTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"