# src\file_conversor\config\log.py

import re
import logging
import tempfile
import shutil

from rich import print

from logging import Handler
from concurrent_log_handler import ConcurrentTimedRotatingFileHandler

from types import TracebackType
from typing import Mapping

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
    LEVEL_CRITICAL, LEVEL_FATAL = logging.CRITICAL, logging.FATAL  # 50
    LEVEL_ERROR = logging.ERROR  # 40
    LEVEL_WARNING = logging.WARNING  # 30
    LEVEL_INFO = logging.INFO  # 20
    LEVEL_DEBUG = logging.DEBUG  # 10

    # logfile name
    FILENAME = f".file_conversor.log"

    @classmethod
    def get_instance(cls, dest_folder: str | Path | None = ".", level: int = LEVEL_INFO):
        """
        Initialize logfile instance

        :param dest_folder: Destination folder to store log file. If None, do not log to file. Defaults to '.' (log to current working folder).
        :param level: Log level. Defaults to LEVEL_INFO.
        """
        return super().get_instance(dest_folder=dest_folder, level=level)

    def __init__(self, dest_folder: str | Path | None, level: int) -> None:
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
        self.set_level(level)
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

    def get_level(self) -> int:
        return logging.getLogger().level

    def set_level(self, level: int):
        logging.getLogger().setLevel(level)

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
