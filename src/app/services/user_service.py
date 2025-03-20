from typing import Any
from datetime import datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.repositories import UserRepository
from app.schemas import UserCreate, UserUpdate
from app.utils import NotFoundError, get_session


class UserService:
    """Service layer for user-related operations."""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.user_repository = UserRepository(session)

    async def get_user_by_uid(self, uid: str) -> User | None:
        """Fetches user by UID."""
        user = await self.user_repository.get_user_by_uid(uid)
        if not user:
            raise NotFoundError(f"User with uid {uid}")
        return user

    async def sync_user(self, user_info: dict[str, Any]) -> User:
        """
        Synchronizes a user from Firebase.
        If the user exists, updates their info; otherwise, creates a new one.
        """
        uid, email = user_info["uid"], user_info["email"]
        existing_user = await self.user_repository.get_user_by_uid(uid)

        if existing_user:
            update_data = UserUpdate(email=email, dt_updated=datetime.now())
            return await self.user_repository.update_user(existing_user, update_data)

        new_user_data = UserCreate(uid=uid, email=email)
        return await self.user_repository.create_user(new_user_data)
