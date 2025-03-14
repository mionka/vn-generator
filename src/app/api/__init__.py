from app.api.health_check import api_router as health_router
from app.api.user import api_router as user_router


list_of_routes = [health_router, user_router]


__all__ = [
    "list_of_routes",
]
