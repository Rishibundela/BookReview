from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from src.config import Config



print("URL:", Config.DATABASE_URL)

engine: AsyncEngine = create_async_engine(
    Config.DATABASE_URL,   # ❗ NO parentheses
    echo=True
)

async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)
