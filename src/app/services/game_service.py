import shutil
from pathlib import Path
from typing import Sequence
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.utils import get_settings
from app.db.models import Game
from app.repositories import GameRepository, UserRepository
from app.schemas import GameCreate
from app.utils import get_session, NotFoundError


class GameService:
    """Service layer for game-related operations."""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.game_repository = GameRepository(session)
        self.user_repository = UserRepository(session)

    async def check_game_exists(self, game_id: UUID) -> bool:
        game = await self.game_repository.get_game_by_id(game_id)
        return game is not None

    async def get_all_games(self) -> Sequence[Game]:
        return await self.game_repository.get_all_games()

    async def add_game(self, game_info: GameCreate, author_uid: str) -> Game | None:
        settings = get_settings()

        author = await self.user_repository.get_user_by_uid(author_uid)
        if not author:
            raise NotFoundError("Author not found.")

        game = await self.game_repository.create_game(game_info, author.id)
        game.author = author
        game_dir = settings.GAME_PATH / str(game.id)
        try:
            self._create_game_files(game_dir, settings.TEMPLATE_PATH)
        except Exception:
            await self.game_repository.delete_game(game.id)
            raise
        return game

    def _create_game_files(self, game_dir: Path, template_dir: Path) -> None:
        if not template_dir.exists():
            raise FileNotFoundError(f"Template game directory not found: {template_dir}.")

        if game_dir.exists():
            shutil.rmtree(game_dir)

        shutil.copytree(template_dir, game_dir)
