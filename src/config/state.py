# src\config\state.py

from typing import Any

# user provided imports
from config.log import Log
from config.locale import get_translation

# Get app config
LOG = Log.get_instance()

_ = get_translation()

logger = LOG.getLogger(__name__)


# STATE ACTIONS
def disable_log(value):
    if not value:
        return
    logger.info(f"{_('File logging')}: [blue red]{_('DISABLED')}[/]")
    LOG.set_dest_folder(None)


def disable_progress(value):
    if not value:
        return
    logger.info(f"{_('Progress bars')}: [blue red]{_('DISABLED')}[/]")


def enable_quiet_mode(value):
    if not value:
        return
    logger.info(f"{_('Quiet mode')}: [blue bold]{_('ENABLED')}[/]")
    LOG.set_level(Log.LEVEL_ERROR)


def enable_verbose_mode(value):
    if not value:
        return
    logger.info(f"{_('Verbose mode')}: [blue bold]{_('ENABLED')}[/]")
    LOG.set_level(Log.LEVEL_INFO)


def enable_debug_mode(value):
    if not value:
        return
    logger.info(f"{_('Debug mode')}: [blue bold]{_('ENABLED')}[/]")
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
        self.__data = {
            # app EXE binary
            "script_executable": "NOT_SET",
            "script_workdir": "NOT_SET",

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
            raise KeyError(f"{_('Key')} '{key}' {_('not found in STATE')}")
        return self.__data[key]

    def __setitem__(self, key, value):
        if key not in self.__data:
            raise KeyError(f"{_('Key')} '{key}' {_('is not a valid key for STATE. Valid options are')} {', '.join(self.__data.keys())}")
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
