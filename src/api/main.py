from fastapi import FastAPI

from api.routers.telemetry import router as telemetry_router
from api.core.settings import get_settings
from api.core.lifespan import lifespan

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(telemetry_router, prefix=settings.api_prefix)
