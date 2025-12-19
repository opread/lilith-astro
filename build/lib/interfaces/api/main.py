"""FastAPI application entry point."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config.settings import Settings
from src.core.domain.exceptions import DomainException


def create_app(settings: Settings) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        settings: Application settings.

    Returns:
        The configured FastAPI app.
    """
    app = FastAPI(
        title="AstroPersona API",
        version="1.0.0",
        description="Personalized horoscope generation API"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An internal error occurred.",
                    "details": str(exc)
                }
            }
        )

    # Include routers
    from .v1 import router as v1_router
    app.include_router(v1_router, prefix="/api")

    # Health check
    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


# Create the app instance
settings = Settings()
app = create_app(settings)