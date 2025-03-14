from pydantic import UUID4, BaseModel, ConfigDict

from app.schemas.user import UserResponse


class BaseGame(BaseModel):
    title: str
    description: str
    cover_image: str

    model_config = ConfigDict(from_attributes=True)


class GameCreate(BaseGame):
    pass


class GameResponse(BaseGame):
    id: UUID4
    author: UserResponse
