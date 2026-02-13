from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
from typing import AsyncGenerator

engine: AsyncEngine = create_async_engine(
    Config.DATABASE_URL,
    echo=True
)

# Create session factory once (standard practice)
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,  # Use the correct session class for async operations
    expire_on_commit=False,
)


async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
