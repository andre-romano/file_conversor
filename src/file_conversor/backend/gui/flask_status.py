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
    def __init__(
            self,
            id: str | int,
            status: str = '',
            message: str = '',
            exception: str = '',
            progress: int | None = None,
    ) -> None:
        super().__init__()
        self._id = str(id)
        self._status = status
        self._message = message
        self._exception = exception
        self._progress = progress

    def __repr__(self) -> str:
        return f"FlaskStatus(id={self._id}, status={self._status}, message={self._message}, exception={self._exception}, progress={self._progress})"

    def __str__(self) -> str:
        return self.__repr__()

    def get_id(self) -> str:
        return self._id

    def get_status(self) -> str:
        return self._status

    def get_message(self) -> str:
        return self._message

    def get_exception(self) -> str:
        return self._exception

    def get_progress(self) -> int | None:
        return self._progress

    def set_progress(self, progress: int) -> None:
        self._progress = progress

    def set(self, other: 'FlaskStatus') -> None:
        self._status = other._status
        self._message = other._message
        self._exception = other._exception
        self._progress = other._progress

    def json(self) -> dict[str, Any]:
        return {
            'id': self._id,
            'status': self._status,
            'message': self._message,
            'exception': self._exception,
            'progress': self._progress,
        }


class FlaskStatusCompleted(FlaskStatus):
    def __init__(self, id: str | int) -> None:
        super().__init__(
            id=id,
            status='completed',
            message=_('Completed'),
            progress=100,
        )


class FlaskStatusProcessing(FlaskStatus):
    def __init__(self, id: str | int, progress: int | None = None) -> None:
        super().__init__(
            id=id,
            status='processing',
            message=_('Processing'),
            progress=progress,
        )


class FlaskStatusReady(FlaskStatus):
    def __init__(self) -> None:
        super().__init__(
            id='0',
            status='ready',
            message=_('Ready'),
        )


class FlaskStatusError(FlaskStatus):
    def __init__(self, id: str | int, exception: str, progress: int | None = None) -> None:
        super().__init__(
            id=id,
            status='failed',
            message=_('Failed'),
            exception=exception,
            progress=progress,
        )


class FlaskStatusUnknown(FlaskStatus):
    def __init__(self, id: str | int) -> None:
        super().__init__(
            id=id,
            status='unknown',
            message=_('Unknown ID'),
            exception=_('The provided status ID does not exist.'),
        )


__all__ = [
    'FlaskStatus',
    'FlaskStatusCompleted',
    'FlaskStatusProcessing',
    'FlaskStatusReady',
    'FlaskStatusError',
    'FlaskStatusUnknown',
]
