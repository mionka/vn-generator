from typing import Sequence
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Game
from app.schemas import GameCreate


class GameRepository:
    """Repository layer responsible for game-related operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_game_by_id(self, game_id: UUID) -> Game | None:
        """Fetches game by ID."""
        query = select(Game).where(Game.id == game_id)
        return await self.session.scalar(query)

    async def get_all_games(self) -> Sequence[Game]:
        """Fetches all games."""
        query = select(Game).options(
            selectinload(Game.author),
        )
        return (await self.session.execute(query)).scalars().all()

    async def create_game(self, game_info: GameCreate, author_id: UUID) -> Game:
        """Creates a new game."""
        game = Game(**game_info.model_dump(), author_id=author_id)
        self.session.add(game)
        await self.session.commit()
        await self.session.refresh(game)
        return game

    async def delete_game(self, game_id: UUID) -> None:
        query = delete(Game).where(Game.id == game_id)
        await self.session.execute(query)
        await self.session.commit()
