from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schemas import UserCreate, UserUpdate


class UserRepository:
    """Repository layer responsible for user-related operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_uid(self, uid: str) -> User | None:
        """Fetches user by UID."""
        query = select(User).where(User.uid == uid)
        return await self.session.scalar(query)

    async def create_user(self, user_data: UserCreate) -> User:
        """Creates a new user."""
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user: User, update_data: UserUpdate) -> User:
        """Updates user information."""
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user
