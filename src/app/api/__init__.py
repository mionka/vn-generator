from .game import api_router as game_router
from .health_check import api_router as health_router
from .user import api_router as user_router
from .run_game import api_router as rungame_router


list_of_routes = [health_router, user_router, game_router, rungame_router]


__all__ = [
    "list_of_routes",
]
