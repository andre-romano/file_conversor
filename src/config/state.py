# src\config\state.py

import sys
from pathlib import Path
from typing import Any

# user provided imports
from config.log import Log

# Get app config
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


def get_script_path() -> Path:
    """Get the absolute path of the currently running script."""
    # 1. Check for frozen executables (PyInstaller)
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve()

    # 3. Check sys.argv[0] (works when run directly)
    if len(sys.argv) > 0 and sys.argv[0]:
        script_path = Path(sys.argv[0]).resolve()
        if script_path.exists():
            return script_path

    # fallback
    return Path().cwd()


def get_executable() -> tuple[str, str]:
    path = get_script_path()
    if path.suffix == ".py":
        idx = path.parts.index("src")
        root_folder = Path(*path.parts[:idx])

        python_bin = (root_folder / ".venv/Scripts/python").resolve()
        return f'"{python_bin}" "{path}"', str(root_folder)
    else:
        root_folder = path.parent.resolve()
        return str(path), str(root_folder)


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
    def get_instance():
        if not State.__instance:
            State.__instance = State()
        return State.__instance

    def __init__(self) -> None:
        super().__init__()
        self.__init_state()

    def __init_state(self):
        # Define state dictionary
        executable, folder = get_executable()
        self.__data = {
            # app EXE binary
            "script_executable": executable,
            "script_folder": folder,
            "icons_folder": str(Path(folder) / 'icons'),

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
        if key in self.__callbacks:
            self.__callbacks[key](value)

    def __contains__(self, key) -> bool:
        return key in self.__data

    def __len__(self) -> int:
        return len(self.__data)

    def update(self, new: dict):
        for key, value in new.items():
            self[key] = value
