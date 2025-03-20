from fastapi import FastAPI
from firebase_admin import credentials, initialize_app
from uvicorn import run

from app.api import list_of_routes
from app.config import DefaultSettings, get_settings
from app.middlewares import list_of_middlewares
from app.utils import exception_handlers, get_hostname


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def add_exception_handlers(application: FastAPI) -> None:
    for exception, handler in exception_handlers:
        application.add_exception_handler(exception, handler)


def add_middlewared(application: FastAPI) -> None:
    for middleware in list_of_middlewares:
        application.add_middleware(middleware)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Template FastAPI service."

    tags_metadata = [
        {
            "name": "Application Health",
            "description": "API health check.",
        },
    ]

    application = FastAPI(
        title="Template App",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="0.1.0",
        openapi_tags=tags_metadata,
    )
    settings = get_settings()
    bind_routes(application, settings)
    add_exception_handlers(application)
    add_middlewared(application)
    application.state.settings = settings
    cred = credentials.Certificate(settings.GOOGLE_APPLICATION_CREDENTIALS)
    initialize_app(cred)
    return application


app = get_app()

if __name__ == "__main__":
    settings_for_application = get_settings()
    run(
        "app.__main__:app",
        host=get_hostname(settings_for_application.APP_HOST),
        port=settings_for_application.APP_PORT,
        reload=True,
        reload_dirs=["app"],
        log_level="debug",
    )
