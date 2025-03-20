from typing import Callable
from fastapi import Response, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DatabaseError, IntegrityError, OperationalError
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except FileNotFoundError:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Template game directory not found."},
            )
        except (OperationalError, OSError):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Database connection error occured."},
            )
        except IntegrityError:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Database integrity error occured."}
            )
        except DatabaseError:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Database error occured."}
            )
        except Exception as exc:  #pylint: disable=broad-exception-caught
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": f"Unexpected error occured: {str(exc)}"},
            )
