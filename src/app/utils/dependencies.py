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
    print("lalala 1")
    try:
        if not token:
            print("lalala no token")
            raise ValueError("Token is missing.")
        print("lalala yes token", token.credentials)
        user = verify_id_token(token.credentials)
        print("lalala token verified")
        return user
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in or invalid credentials.",
        ) from exc
