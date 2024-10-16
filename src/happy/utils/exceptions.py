"""Loggable exceptions."""

import json
import uuid
from typing import Any


class LoggableError(Exception):
    """Generic Loggable exception with traceable id."""

    default_message: str = None

    def __init__(self, error: str = None) -> None:
        if error is None:
            error = self.default_message

        data = {
            "error": error,
            "id": str(uuid.uuid4()),
        }

        super().__init__(json.dumps(data))


class PermissionCheckError(LoggableError):
    """Error raised when permissions checks fail."""

    def __init__(
        self, username: str, fields: list[str] | tuple[str] | dict[str, Any]
    ) -> None:
        error = {
            "message": f"{username} lacks permission to access fields",
            "fields": fields,
        }
        super().__init__(error)
