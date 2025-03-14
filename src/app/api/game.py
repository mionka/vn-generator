from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import TypeAdapter
from starlette import status

from app.schemas import GameCreate, GameResponse
from app.services import GameService
from app.utils import get_firebase_user_from_token, NotFoundError


api_router = APIRouter(
    prefix="/game",
    tags=["Game"],
)


@api_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[GameResponse],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials.",
        },
    },
)
async def search_games(
    _: dict = Depends(get_firebase_user_from_token),
    game_service: GameService = Depends(),
) -> List[GameResponse]:
    games = await game_service.get_all_games()
    return TypeAdapter(List[GameResponse]).validate_python(games)


@api_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=GameResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials.",
        },
    },
)
async def add_game(
    game_info: GameCreate = Body(...),
    current_user: dict = Depends(get_firebase_user_from_token),
    game_service: GameService = Depends(),
) -> GameResponse:
    try:
        game = await game_service.add_game(game_info, current_user["uid"])
        return game
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
