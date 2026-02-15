from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
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
    password_hash: str = Field(exclude=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False))

    def __repr__(self):
        return f"<User {self.username}>"