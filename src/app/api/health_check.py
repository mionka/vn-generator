from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.schemas import MessageSuccess
from app.services import HealthCheckService


api_router = APIRouter(
    prefix="/health_check",
    tags=["Application Health"],
)


@api_router.get(
    "/ping_application",
    response_model=MessageSuccess,
    status_code=status.HTTP_200_OK,
)
async def ping_application() -> MessageSuccess:
    """Checks if the application is working."""
    return MessageSuccess(message="Application works!")


@api_router.get(
    "/ping_database",
    response_model=MessageSuccess,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Database does not work.",
        },
    },
)
async def ping_database(
    health_service: HealthCheckService = Depends(),
) -> MessageSuccess:
    """Checks if the database is reachable and working."""
    if await health_service.check_database():
        return MessageSuccess(message="Database works!")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database does not work.",
    )
