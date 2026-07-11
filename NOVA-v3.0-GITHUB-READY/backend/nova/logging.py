"""Centralized, structured logging for NOVA services."""

from __future__ import annotations

import json
import logging
import logging.config
from datetime import UTC, datetime
from typing import Any

from nova.config import LogFormat, Settings


class JsonFormatter(logging.Formatter):
    """Serialize log records as one-line JSON for production ingestion."""

    _reserved = frozenset(logging.makeLogRecord({}).__dict__)

    def format(self, record: logging.LogRecord) -> str:
        """Convert a log record to a stable JSON document."""
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        payload.update(
            {
                key: value
                for key, value in record.__dict__.items()
                if key not in self._reserved and key not in {"message", "asctime"}
            }
        )
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, ensure_ascii=False, separators=(",", ":"))


def configure_logging(settings: Settings) -> None:
    """Configure root logging once from validated application settings."""
    formatter_name = "json" if settings.log_format is LogFormat.JSON else "console"
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {"()": "nova.logging.JsonFormatter"},
                "console": {
                    "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": formatter_name,
                    "level": settings.log_level,
                    "stream": "ext://sys.stdout",
                }
            },
            "root": {"handlers": ["console"], "level": settings.log_level},
        }
    )

