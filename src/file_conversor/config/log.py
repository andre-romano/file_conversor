# src\file_conversor\config\log.py

import re
import logging
import tempfile
import shutil

from rich import print

from logging import Handler
from concurrent_log_handler import ConcurrentTimedRotatingFileHandler

from enum import Enum
from types import TracebackType
from typing import Mapping, Self

from pathlib import Path

# user-provided imports
from file_conversor.config.abstract_singleton_thread_safe import AbstractSingletonThreadSafe


class Log(AbstractSingletonThreadSafe):
    class CustomLogger:
        def __init__(self, name: str | None) -> None:
            super().__init__()
            self._name = name
            self._log_to_file = True

        @property
        def _logger(self):
            return logging.getLogger(self._name)

        @property
        def level(self) -> int:
            if self._logger.level > logging.NOTSET:
                return self._logger.level
            return logging.getLogger().level

        @property
        def log_to_file(self) -> bool:
            return self._log_to_file

        @log_to_file.setter
        def log_to_file(self, value: bool):
            self._log_to_file = value

        def critical(self, msg: object, *args: object, exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
            if self.log_to_file:
                self._logger.critical(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
            if self.level <= logging.CRITICAL:
                print(f"[bold reverse red][CRITICAL][/]: {msg}")

        def fatal(self, msg: object, *args: object, exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
            if self.log_to_file:
                self._logger.fatal(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
            if self.level <= logging.FATAL:
                print(f"[bold reverse red][FATAL][/]: {msg}")

        def error(self, msg: object, *args: object, exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
            if self.log_to_file:
                self._logger.error(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
            if self.level <= logging.ERROR:
                print(f"[bold red][ERROR][/]: {msg}")

        def warning(self, msg: object, *args: object, exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
            if self.log_to_file:
                self._logger.warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
            if self.level <= logging.WARNING:
                print(f"[bold yellow][WARN][/]: {msg}")

        def info(self, msg: object, *args: object, exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
            if self.log_to_file:
                self._logger.info(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
            if self.level <= logging.INFO:
                print(f"[bold white][INFO][/]: {msg}")

        def debug(self, msg: object, *args: object, exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
            if self.log_to_file:
                self._logger.debug(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
            if self.level <= logging.DEBUG:
                print(f"[bold cyan][DEBUG][/]: {msg}")

    class StripMarkupFormatter(logging.Formatter):
        # Use a custom formatter that strips Rich markup
        TAG_RE = re.compile(r'\[/?[^\]]+\]')  # matches [tag] and [/tag]

        def format(self, record):
            if isinstance(record.msg, str):
                record.msg = self.TAG_RE.sub('', record.msg)
            return super().format(record)

    # most severe level, to least
    class Level(Enum):
        """ Log levels enum """
        CRITICAL = logging.CRITICAL
        """ 50 = Critical logging level """
        FATAL = logging.FATAL
        """ 50 = Fatal logging level """
        ERROR = logging.ERROR
        """ 40 = Error logging level """
        WARNING = logging.WARNING
        """ 30 = Warning logging level """
        INFO = logging.INFO
        """ 20 = Verbose logging level """
        DEBUG = logging.DEBUG
        """ 10 = Debug logging level """

        @classmethod
        def get(cls) -> Self:
            return cls(logging.getLogger().level)

        def set(self) -> Self:
            logging.getLogger().setLevel(self.value)
            if self.value != self.get().value:
                raise RuntimeError(f"Unable to set log level to {self.name} ({self.value}). Current level is {self.get()}.")
            return self

        def is_critical(self) -> bool:
            return self.value <= Log.Level.CRITICAL.value

        def is_quiet(self) -> bool:
            return self.value <= Log.Level.ERROR.value

        def is_verbose(self) -> bool:
            return self.value <= Log.Level.INFO.value

        def is_debug(self) -> bool:
            return self.value <= Log.Level.DEBUG.value

    # logfile name
    FILENAME = f".file_conversor.log"

    @classmethod
    def get_instance(cls, dest_folder: str | Path | None = ".", level: Level = Level.INFO):
        """
        Initialize logfile instance

        :param dest_folder: Destination folder to store log file. If None, do not log to file. Defaults to '.' (log to current working folder).
        :param level: Log level. Defaults to LEVEL_INFO.
        """
        return super().get_instance(dest_folder=dest_folder, level=level)

    def __init__(self, dest_folder: str | Path | None, level: Level) -> None:
        """
        Initialize logfile, inside a dest_folder with a log_level
        """
        super().__init__()
        self._dest_path: Path | None = None
        self._file_handler: Handler | None = None
        self._lock_file_dir = Path(tempfile.mkdtemp()).resolve()

        # configure logger
        self._log_formatter = Log.StripMarkupFormatter(
            fmt='[%(asctime)s] - [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # set level
        self._level = level.set()
        self.set_dest_folder(dest_folder)

    def shutdown(self):
        logging.shutdown()
        try:
            if self._lock_file_dir.exists():
                shutil.rmtree(self._lock_file_dir)
        except PermissionError:
            pass

    def getLogger(self, name: str | None = None) -> CustomLogger:
        return Log.CustomLogger(name)

    def get_dest_folder(self) -> Path | None:
        return self._dest_path

    def set_dest_folder(self, dest_folder: str | Path | None):
        """Activates / deactivates file logging, and sets destination folder"""
        if not dest_folder:
            self._remove_handler(self._file_handler)
            self._dest_path = None
            self._file_handler = None
            return

        self._dest_path = Path(dest_folder).resolve()

        self._file_handler = ConcurrentTimedRotatingFileHandler(
            filename=(self._dest_path / Log.FILENAME).resolve(),
            when='midnight',     # rotate at midnight
            interval=1,          # every 1 day
            backupCount=7,       # keep 7 days of logs
            encoding='utf-8',
            utc=False,           # set to True if you want UTC-based rotation
            lock_file_directory=str(self._lock_file_dir),
        )
        self._add_handler(self._file_handler)

    def _remove_handler(self, handler: Handler | None):
        if handler:
            logging.getLogger().removeHandler(handler)

    def _add_handler(self, handler: Handler):
        handler.setFormatter(self._log_formatter)
        logging.getLogger().addHandler(handler)


__all__ = [
    "Log",
]
