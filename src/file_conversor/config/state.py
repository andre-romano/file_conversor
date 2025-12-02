# src\file_conversor\config\state.py

from pathlib import Path

from typing import Any

# user provided imports
from file_conversor.config.log import Log

from file_conversor.config.abstract_singleton_thread_safe import AbstractSingletonThreadSafe

# Get app config
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


# STATE ACTIONS
def disable_log(value):
    if not value:
        return
    logger.info(f"'File logging': [blue red]'DISABLED'[/]")
    LOG.set_dest_folder(None)


def disable_progress(value):
    if not value:
        return
    logger.info(f"Progress bars: [blue red]DISABLED[/]")


def enable_quiet_mode(value):
    if not value:
        return
    logger.info(f"Quiet mode: [blue bold]ENABLED[/]")
    LOG.set_level(Log.LEVEL_ERROR)


def enable_verbose_mode(value):
    if not value:
        return
    logger.info(f"Verbose mode: [blue bold]ENABLED[/]")
    LOG.set_level(Log.LEVEL_INFO)


def enable_debug_mode(value):
    if not value:
        return
    logger.info(f"Debug mode: [blue bold]ENABLED[/]")
    LOG.set_level(Log.LEVEL_DEBUG)


def enable_overwrite_output_mode(value):
    if not value:
        return
    logger.info(f"Output overwrite mode: [blue bold]ENABLED[/]")


# STATE controller dict class
class State(AbstractSingletonThreadSafe):
    def __init__(self) -> None:
        super().__init__()
        self.__init_state()

    def __init_state(self):
        # Define state dictionary
        self.__data = {
            # app options
            "no-log": False,
            "no-progress": False,
            "quiet": False,
            "verbose": False,
            "debug": False,
            "overwrite-output": False,
        }
        self.__callbacks = {
            "no-log": disable_log,
            "no-progress": disable_progress,
            "quiet": enable_quiet_mode,
            "verbose": enable_verbose_mode,
            "debug": enable_debug_mode,
            "overwrite-output": enable_overwrite_output_mode,
        }
        # run callbacks
        for key, value in self.__data.items():
            self._run_callbacks(key=key, value=value)

    def _run_callbacks(self, key: str, value):
        if key in self.__callbacks:
            self.__callbacks[key](value)

    def __repr__(self) -> str:
        return repr(self.__data)

    def __str__(self) -> str:
        return str(self.__data)

    def __getitem__(self, key) -> Any:
        if key not in self.__data:
            raise KeyError(f"Key '{key}' not found in STATE")
        return self.__data[key]

    def __setitem__(self, key, value):
        if key not in self.__data:
            raise KeyError(f"Key '{key}' is not a valid key for STATE. Valid options are {', '.join(self.__data.keys())}")
        self.__data[key] = value

        # run callback
        self._run_callbacks(key=key, value=value)

    def __contains__(self, key) -> bool:
        return key in self.__data

    def __len__(self) -> int:
        return len(self.__data)

    def to_dict(self) -> dict[str, Any]:
        return self.__data.copy()

    def update(self, new: dict):
        for key, value in new.items():
            self[key] = value


__all__ = [
    "State",
]
