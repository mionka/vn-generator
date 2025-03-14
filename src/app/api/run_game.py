from fastapi import APIRouter, Depends, HTTPException, Path
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
            "description": "Could find the game.",
        },
    },
)
async def get_game(
    game_id: UUID4 = Path(...),
    game_service: GameService = Depends(),
    # _: User = Depends(get_firebase_user_from_token),
) -> FileResponse:
    filename = "index.html"
    if not await game_service.check_game_exists(game_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )

    if not game_service.game_file_exists(game_id, filename):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game file not found: {filename}",
        )

    return FileResponse(game_service.get_game_filepath(game_id, filename))


@api_router.get(
    "/{filepath:path}",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials.",
        },
    },
)
async def get_game_file(
    game_id: UUID4 = Path(...),
    filepath: str = Path(...),
    game_service: GameService = Depends(),
) -> FileResponse:
    if not game_service.game_file_exists(game_id, filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File {filepath} not found",
        )

    return FileResponse(game_service.get_game_filepath(game_id, filepath))
