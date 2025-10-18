# src\file_conversor\backend\gui\flask_status.py

from flask import Flask
from typing import Any, Callable, Self

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import AVAILABLE_LANGUAGES, get_system_locale, get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


class FlaskStatus:
    @classmethod
    def get_status_ready(cls) -> Self:
        return cls(
            id="0",
            status='ready',
            message='Ready',
            exception='',
            progress=None,
        )

    @classmethod
    def get_status_unknown(cls, id: str | int) -> Self:
        return cls(
            id=id,
            status='failed',
            message=_('Error'),
            exception=f"{_('Status ID')} '{id}' {_('does not exist.')}",
            progress=None,
        )

    def __init__(
            self,
            id: str | int,
            status: str,
            message: str,
            exception: str = '',
            progress: int | None = None,
    ) -> None:
        super().__init__()
        self.id = str(id)
        self.status = status
        self.message = message
        self.exception = exception
        self.progress = progress

    def __repr__(self) -> str:
        return f"FlaskStatus(id={self.id}, status={self.status}, message={self.message}, exception={self.exception}, progress={self.progress})"

    def __str__(self) -> str:
        return self.__repr__()

    def json(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'status': self.status,
            'message': self.message,
            'exception': self.exception,
            'progress': self.progress,
        }


__all__ = ["FlaskStatus"]
