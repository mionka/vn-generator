from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession


class HealthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_database_health(self) -> bool:
        health_check_query = select(text("1"))
        result = await self.session.scalars(health_check_query)
        return result is not None
