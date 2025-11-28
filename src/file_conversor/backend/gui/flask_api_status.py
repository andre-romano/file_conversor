# src\file_conversor\backend\gui\flask_api_status.py

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


class FlaskApiStatus:
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

    def __eq__(self, value) -> bool:
        if not isinstance(value, FlaskApiStatus):
            return False
        return (self._id == value._id and
                self._status == value._status)

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

    def set_progress(self, progress: int | float) -> None:
        self._progress = int(progress)

    def set_message(self, message: str) -> None:
        self._message = message

    def set(self, other: 'FlaskApiStatus') -> None:
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


class FlaskApiStatusCompleted(FlaskApiStatus):
    def __init__(
            self,
            id: str | int,
            message: str = "",
    ) -> None:
        super().__init__(
            id=id,
            status='completed',
            message=message,
            progress=100,
        )


class FlaskApiStatusProcessing(FlaskApiStatus):
    def __init__(
            self,
            id: str | int,
            progress: int | None = None,
            message: str = "",
    ) -> None:
        super().__init__(
            id=id,
            status='processing',
            message=message,
            progress=progress,
        )


class FlaskApiStatusReady(FlaskApiStatus):
    def __init__(self) -> None:
        super().__init__(
            id='0',
            status='ready',
        )


class FlaskApiStatusError(FlaskApiStatus):
    def __init__(
            self,
            id: str | int,
            exception: str,
            progress: int | None = None,
    ) -> None:
        super().__init__(
            id=id,
            status='failed',
            exception=exception,
            progress=progress,
        )


class FlaskApiStatusUnknown(FlaskApiStatus):
    def __init__(
            self,
            id: str | int,
    ) -> None:
        super().__init__(
            id=id,
            status='unknown',
            exception=_('The provided status ID does not exist.'),
        )


__all__ = [
    'FlaskApiStatus',
    'FlaskApiStatusCompleted',
    'FlaskApiStatusProcessing',
    'FlaskApiStatusReady',
    'FlaskApiStatusError',
    'FlaskApiStatusUnknown',
]
