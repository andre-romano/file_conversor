# src\file_conversor\config\state.py

import shutil
import sys

from pathlib import Path
from importlib.resources import files

from typing import Any

# user provided imports
from file_conversor.config.log import Log

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


# STATE controller dict class
class State:
    __instance = None

    @staticmethod
    def get_executable() -> str:
        """Get the executable path for this app's CLI."""
        res = ""

        exe = shutil.which(sys.argv[0]) if sys.argv else None
        if exe and not exe.endswith(".py"):
            res = rf'"{exe}"'
        else:
            python_exe = sys.executable
            main_py = Path(rf"{State.get_resources_folder()}/__main__.py")
            res = rf'"{python_exe}" "{main_py}"'

        logger.debug(f"Executable cmd: {res}")
        return res

    @staticmethod
    def get_resources_folder() -> Path:
        """Get the absolute path of the included folders in pip."""
        res_path = Path(str(files("file_conversor"))).resolve()
        return res_path

    @staticmethod
    def get_icons_folder() -> Path:
        """Get the absolute path of the included folders in pip."""
        icons_path = State.get_resources_folder() / ".icons"
        logger.debug(f"Icons path: {icons_path}")
        return icons_path

    @staticmethod
    def get_locales_folder() -> Path:
        locales_path = State.get_resources_folder() / ".locales"
        logger.debug(f"Locales path: {locales_path}")
        return locales_path

    @staticmethod
    def get_instance():
        if not State.__instance:
            State.__instance = State()
        return State.__instance

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
        }
        self.__callbacks = {
            "no-log": disable_log,
            "no-progress": disable_progress,
            "quiet": enable_quiet_mode,
            "verbose": enable_verbose_mode,
            "debug": enable_debug_mode,
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

    def update(self, new: dict):
        for key, value in new.items():
            self[key] = value
