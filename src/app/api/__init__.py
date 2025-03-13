from app.api.health_check import api_router as health_router


list_of_routes = [
    health_router,
]


__all__ = [
    "list_of_routes",
]
