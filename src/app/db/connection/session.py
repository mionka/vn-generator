from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls) -> "SessionManager":
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance  # noqa

    def get_session_maker(self) -> async_sessionmaker:
        return async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

    def refresh(self) -> None:
        self.engine = create_async_engine(get_settings().database_uri, echo=True, future=True)
