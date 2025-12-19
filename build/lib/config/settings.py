"""Application settings using Pydantic."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_env: str = "development"
    swiss_eph_path: str = "/usr/local/share/sweph"
    google_api_key: str

    class Config:
        env_file = ".env"
        case_sensitive = False