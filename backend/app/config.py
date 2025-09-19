from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = Field("Respir Learning API", description="Displayed name for the API")
    database_url: str = Field(
        "postgresql+psycopg2://postgres:postgres@localhost:5432/respir",
        description="Database connection string. Defaults to a local PostgreSQL instance.",
    )
    admin_api_key: str = Field(
        "change-me",
        description="Static API key protecting administrative endpoints.",
    )
    auto_seed: bool = Field(
        False,
        description=(
            "When true the application will populate the database with demo data "
            "during startup."
        ),
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return a cached instance of :class:`Settings`."""

    return Settings()


settings = get_settings()
