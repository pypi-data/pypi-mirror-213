from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from politikontroller_app.logging import configure_logging
from politikontroller_app.web.api.router import api_router
from politikontroller_app.web.lifetime import (
    register_shutdown_event,
    register_startup_event,
)


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="politikontroller_app",
        version=metadata.version("politikontroller-app"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
