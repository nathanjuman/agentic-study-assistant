from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.logging import configure_logging
from config.settings import get_settings

# structured logger for lifecycle events
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Controls startup/shutdown lifecycle,
    runs once on app startup and once on shutdown.

    Initializes console and file logging when app starts.
    Emits log events on startup and shutdown, handing control
    back to FastAPI while app is running.
    """
    settings = get_settings()
    configure_logging(settings)
    logger.info("app_startup", environment=settings.environment)
    yield
    logger.info("app_shutdown")


def create_app() -> FastAPI:
    """Builds reusable FastAPI instance."""
    app = FastAPI(
        title="Agentic Study Assistant Backend",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        # Verify backend is up
        return {"status": "ok"}

    return app
app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(app, host=settings.api_host, port=settings.api_port, reload=True)
