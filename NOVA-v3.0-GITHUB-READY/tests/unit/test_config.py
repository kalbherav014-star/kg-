"""Unit tests for validated NOVA configuration."""

import pytest
from pydantic import ValidationError

from nova.config import Settings


def test_settings_use_secure_local_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.log_level == "INFO"
    assert "*" not in settings.allowed_origins
    assert str(settings.ollama_base_url) == "http://127.0.0.1:11434/"


def test_log_level_is_normalized() -> None:
    settings = Settings(_env_file=None, log_level="warning")

    assert settings.log_level == "WARNING"


def test_wildcard_origin_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, allowed_origins=("*",))

