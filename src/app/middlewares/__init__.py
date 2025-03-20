from .exception_middleware import ExceptionMiddleware


list_of_middlewares = [
    ExceptionMiddleware,
]


__all__ = [
    "list_of_middlewares",
]
