"""Validated application configuration loaded from environment variables."""

from __future__ import annotations

from enum import StrEnum
from functools import lru_cache
from pathlib import Path

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Supported runtime environments."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class LogFormat(StrEnum):
    """Supported logging output formats."""

    JSON = "json"
    CONSOLE = "console"


class Settings(BaseSettings):
    """NOVA settings with safe defaults and environment validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="NOVA_",
        case_sensitive=False,
        extra="ignore",
    )

    environment: Environment = Environment.DEVELOPMENT
    log_level: str = "INFO"
    log_format: LogFormat = LogFormat.JSON
    data_dir: Path = Path("database")
    allowed_origins: tuple[str, ...] = (
        "http://localhost:8788",
        "http://127.0.0.1:8788",
    )
    ollama_base_url: AnyHttpUrl = AnyHttpUrl("http://127.0.0.1:11434")
    ollama_model: str = Field(default="llama3.2", min_length=1, max_length=100)

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        """Normalize and validate standard Python logging levels."""
        normalized = value.upper()
        if normalized not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("log_level must be DEBUG, INFO, WARNING, ERROR, or CRITICAL")
        return normalized

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: object) -> object:
        """Accept comma-separated origins from environment variables."""
        if isinstance(value, str):
            return tuple(origin.strip() for origin in value.split(",") if origin.strip())
        return value

    @field_validator("allowed_origins")
    @classmethod
    def reject_wildcard_origins(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        """Prevent unsafe credentialed cross-origin configurations."""
        if not value:
            raise ValueError("at least one allowed origin is required")
        if "*" in value:
            raise ValueError("wildcard origins are not permitted")
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide immutable-by-convention settings instance."""
    return Settings()

