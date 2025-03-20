from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from .exceptions import NotFoundError


def not_found_error_handler(_: Request, exc: NotFoundError) -> JSONResponse:
    """Handles NotFoundError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )
