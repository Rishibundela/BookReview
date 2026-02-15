from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .utils import hash_password
from .models import User
from .schema import UserCreate

class UserService:
  async def get_user_by_email(self, email: str, session: AsyncSession):

    statement = select(User).where(User.email == email)
    result = await session.exec(statement)

    return result.first()  # Returns the first matching user or None if not found
  
  async def user_exists(self, email: str, session: AsyncSession):
    user = await self.get_user_by_email(email, session)
    return True if user is not None else False
  
  async def create_user(self, user_data: UserCreate, session: AsyncSession):


      new_user = User(
          username=user_data.username,
          email=user_data.email,
          first_name=user_data.first_name,
          last_name=user_data.last_name,
          password_hash=hash_password(user_data.password),
          role="user"
      )

      session.add(new_user)
      await session.commit()
      await session.refresh(new_user)

      return new_user
