# src\config\log.py

import re
import logging

from rich import print

from logging import Handler
from logging.handlers import TimedRotatingFileHandler

from types import TracebackType
from typing import Mapping

from pathlib import Path


class Log:
    class CustomLogger:
        def __init__(self, name: str | None) -> None:
            super().__init__()
            self._name = name

        @property
        def _logger(self):
            return logging.getLogger(self._name)

        @property
        def level(self):
            if self._logger.level > logging.NOTSET:
                return self._logger.level
            return logging.getLogger().level

        def critical(self, msg: object, *args: object, exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
            self._logger.critical(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
            if self.level <= logging.CRITICAL:
                print(f"[bold reverse red][CRITICAL][/]: {msg}")

        def fatal(self, msg: object, *args: object, exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
            self._logger.fatal(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
            if self.level <= logging.FATAL:
                print(f"[bold reverse red][FATAL][/]: {msg}")

        def error(self, msg: object, *args: object, exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
            self._logger.error(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
            if self.level <= logging.ERROR:
                print(f"[bold red][ERROR][/]: {msg}")

        def warning(self, msg: object, *args: object, exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
            self._logger.warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
            if self.level <= logging.WARNING:
                print(f"[bold yellow][WARN][/]: {msg}")

        def info(self, msg: object, *args: object, exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
            self._logger.info(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
            if self.level <= logging.INFO:
                print(f"[bold white][INFO][/]: {msg}")

        def debug(self, msg: object, *args: object, exc_info: None | bool | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
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

    # singleton instance
    __instance = None

    # most severe level, to least
    LEVEL_CRITICAL, LEVEL_FATAL = logging.CRITICAL, logging.FATAL  # 50
    LEVEL_ERROR = logging.ERROR  # 40
    LEVEL_WARNING = logging.WARNING  # 30
    LEVEL_INFO = logging.INFO  # 20
    LEVEL_DEBUG = logging.DEBUG  # 10

    # logfile name
    FILENAME = f".file_conversor.log"

    @staticmethod
    def get_instance(dest_folder: str | Path | None = ".", level: int = LEVEL_INFO):
        """
        Initialize logfile instance

        :param dest_folder: Destination folder to store log file. If None, do not log to file. Defaults to '.' (log to current working folder).
        :param level: Log level. Defaults to LEVEL_INFO.
        """
        if not Log.__instance:
            Log.__instance = Log(dest_folder=dest_folder, level=level)
        return Log.__instance

    def __init__(self, dest_folder: str | Path | None, level: int) -> None:
        """
        Initialize logfile, inside a dest_folder with a log_level
        """
        super().__init__()
        self._dest_path: Path | None
        self._log_file: Path | None

        # configure logger
        self._log_formatter = Log.StripMarkupFormatter(
            fmt='[%(asctime)s] - [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # set level
        self.set_level(level)
        if dest_folder:
            self._set_dest_folder(dest_folder)

    def getLogger(self, name: str | None = None) -> CustomLogger:
        return Log.CustomLogger(name)

    def get_level(self) -> int:
        return logging.getLogger().level

    def set_level(self, level: int):
        logging.getLogger().setLevel(level)

    def get_dest_folder(self) -> Path | None:
        return self._dest_path

    def _set_dest_folder(self, dest_folder: str | Path):
        self._dest_path = Path(dest_folder).resolve()
        self._log_file = (self._dest_path / Log.FILENAME).resolve()

        self._add_handler(TimedRotatingFileHandler(
            filename=self._log_file,
            when='midnight',     # rotate at midnight
            interval=1,          # every 1 day
            backupCount=7,       # keep 7 days of logs
            encoding='utf-8',
            utc=False            # set to True if you want UTC-based rotation
        ))

    def _clear_handlers(self):
        for handler in logging.getLogger().handlers:
            logging.getLogger().removeHandler(handler)

    def _add_handler(self, handler: Handler):
        handler.setFormatter(self._log_formatter)
        logging.getLogger().addHandler(handler)
