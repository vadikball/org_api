"""Application with configuration for events, routers and middleware."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import router
from src.core.settings import app_settings
from src.lifespan.lifespan import app_lifespan


app_description = """
    Organization directory API with geospatial support for searching buildings and companies by coordinates, category, or name.
"""


def get_application() -> FastAPI:
    """Create configured server application instance."""

    application = FastAPI(
        title="Organization Directory API",
        description=app_description,
        root_path="/organization_directory",
        debug=app_settings.DEBUG,
        openapi_url="/openapi.json",
        docs_url="/docs" if app_settings.DEBUG else None,
        lifespan=app_lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router)

    return application


app = get_application()
