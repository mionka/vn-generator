from fastapi import APIRouter, Depends, Path
from fastapi.responses import FileResponse
from pydantic import UUID4
from starlette import status

from app.services import GameService


api_router = APIRouter(
    prefix="/run_game/{game_id}",
    tags=["Run Game"],
)


@api_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Requested resource not found.",
        },
    },
)
async def get_game(
    game_id: UUID4 = Path(...),
    game_service: GameService = Depends(),
    # _: User = Depends(get_firebase_user_from_token),
) -> FileResponse:
    _ = await game_service.get_game(game_id)
    filename = "index.html"
    return FileResponse(game_service.get_game_file(game_id, filename))


@api_router.get(
    "/{filepath:path}",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Requested resource not found.",
        },
    },
)
async def get_game_file(
    game_id: UUID4 = Path(...),
    filepath: str = Path(...),
    game_service: GameService = Depends(),
) -> FileResponse:
    return FileResponse(game_service.get_game_file(game_id, filepath))
