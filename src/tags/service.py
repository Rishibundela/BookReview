from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from src.books.service import BookService
from src.db.models import Tag
from sqlalchemy.orm import selectinload

from .schemas import TagAddModel, TagCreateModel
from src.errors import TagNotFound, TagAlreadyExists, BookNotFound

book_service = BookService()


server_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong"
)


class TagService:

    async def get_tags(self, session: AsyncSession):
        """Get all tags"""

        statement = select(Tag).order_by(desc(Tag.created_at))

        result = await session.exec(statement)

        return result.all()

    async def add_tags_to_book(
        self, book_id: str, tag_data: TagAddModel, session: AsyncSession
    ):
        """Add tags to a book"""

        result = await session.exec(
          select(Book)
          .where(Book.id == book_id)
          .options(selectinload(Book.tags))
      )

        book = result.first()

        if not book:
            raise BookNotFound()

        for tag_item in tag_data.tags:
            result = await session.exec(
                select(Tag).where(Tag.name == tag_item.name)
            )

            tag = result.first()
            if not tag:
                tag = Tag(name=tag_item.name)
                session.add(tag)
                await session.flush() # ensures tag gets ID

            book.tags.append(tag)

        await session.commit()
        await session.refresh(book)
        return book



    async def get_tag_by_id(self, tag_id: str, session: AsyncSession):
        """Get tag by uid"""

        statement = select(Tag).where(Tag.id == tag_id)

        result = await session.exec(statement)

        return result.first()

    async def add_tag(self, tag_data: TagCreateModel, session: AsyncSession):
        """Create a tag"""

        statement = select(Tag).where(Tag.name == tag_data.name)

        result = await session.exec(statement)

        tag = result.first()

        if tag:
            raise TagAlreadyExists()

        new_tag = Tag(name=tag_data.name)

        session.add(new_tag)
        await session.commit()
        await session.refresh(new_tag)
        return new_tag

    async def update_tag(
        self, tag_id: str, tag_update_data: TagCreateModel, session: AsyncSession
    ):
        tag = await self.get_tag_by_id(tag_id, session)

        if not tag:
            raise TagNotFound()

        update_data_dict = tag_update_data.model_dump()

        for k, v in update_data_dict.items():
            setattr(tag, k, v)

        await session.commit()
        await session.refresh(tag)

        return tag


    async def delete_tag(self, tag_id: str, session: AsyncSession):
        tag = await self.get_tag_by_id(tag_id, session)

        if not tag:
            raise TagNotFound()

        await session.delete(tag)
        await session.commit()