from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.schemas import UserResponse
from app.services import UserService
from app.utils import get_firebase_user_from_token


api_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@api_router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials.",
        },
    },
)
async def sync_user(
    current_user: dict = Depends(get_firebase_user_from_token),
    user_service: UserService = Depends(),
) -> UserResponse:
    """Synchronizes the user data based on the Firebase information."""
    user = await user_service.sync_user(current_user)
    return UserResponse.model_validate(user)


@api_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found.",
        },
    },
)
async def get_current_user(
    current_user: dict = Depends(get_firebase_user_from_token),
    user_service: UserService = Depends(),
) -> UserResponse:
    """Retrieves current user information."""
    user = await user_service.get_user_by_uid(current_user["uid"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return UserResponse.model_validate(user)
