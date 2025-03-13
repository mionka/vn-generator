from pydantic import BaseModel


class MessageSuccess(BaseModel):
    message: str
