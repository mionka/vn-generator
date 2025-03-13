from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import SessionManager


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session
