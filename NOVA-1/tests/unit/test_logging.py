"""Unit tests for structured logging."""

import json
import logging

from nova.logging import JsonFormatter


def test_json_formatter_produces_machine_readable_event() -> None:
    record = logging.LogRecord(
        name="nova.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="ready",
        args=(),
        exc_info=None,
    )

    payload = json.loads(JsonFormatter().format(record))

    assert payload["level"] == "INFO"
    assert payload["logger"] == "nova.test"
    assert payload["message"] == "ready"

