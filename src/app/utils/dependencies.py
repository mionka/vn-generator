from typing import Any, AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from firebase_admin.auth import verify_id_token
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.connection import SessionManager


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides an asynchronous database session for FastAPI dependencies."""
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session


def get_firebase_user_from_token(
    token: HTTPAuthorizationCredentials | None = Depends(get_settings().BEARER_SCHEME),
) -> dict[str, Any] | None:
    """Verifies Firebase ID token and returns the authenticated user details."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing.",
        )
    try:
        user = verify_id_token(token.credentials)
        return user
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
        ) from exc
