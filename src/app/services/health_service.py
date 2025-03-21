from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import HealthRepository
from app.utils import get_session


class HealthCheckService:
    """Service layer responsible for health checking."""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.health_repository = HealthRepository(session)

    async def check_database(self) -> bool:
        """Checks if the database is reachable."""
        return await self.health_repository.check_database_health()
