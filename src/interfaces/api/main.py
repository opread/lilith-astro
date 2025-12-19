"""FastAPI application entry point."""

import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

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

    # --- Web App Serving Configuration ---
    # The application expects a static directory at the project root: ./static
    STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'static')
    
    # 1. Mount StaticFiles for assets (e.g., /static/app.js)
    app.mount(
        "/static", StaticFiles(directory=STATIC_DIR), name="static"
    )
    
    # 2. SPA fallback: serve index.html for any unmatched route (including /)
    # This ensures that any route not matching /health, /api, or /static returns index.html for client-side routing.
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa_index(request: Request, full_path: str):
        index_path = os.path.join(STATIC_DIR, "index.html")
        
        # If the index.html exists, serve it for all unmatched routes (SPA client-side routing)
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                html_content = f.read()
            return HTMLResponse(content=html_content, status_code=200)
        
        # If index.html is missing, return a 404 JSON response.
        return JSONResponse(status_code=404, content={"detail": f"Path /{full_path} not found and frontend index.html is unavailable."})

    return app


# Create the app instance
settings = Settings()
app = create_app(settings)