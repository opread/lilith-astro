"""Application settings using Pydantic."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    app_env: str = "development"
    swiss_eph_path: str = ""
    google_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )