
# src\file_conversor\command\win\restart_explorer_cmd.py

from enum import Enum
from typing import Any, Callable

# user-provided modules
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.system import System, WindowsSystem


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WinRestartExplorerCommand:
    EXTERNAL_DEPENDENCIES: set[str] = set()

    class SupportedInFormats(Enum):
        """ empty enum since this command does not process files, but is just a system command to restart explorer.exe """
    class SupportedOutFormats(Enum):
        """ empty enum since this command does not process files, but is just a system command to restart explorer.exe """

    @classmethod
    def restart_explorer(
        cls,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        if isinstance(System, WindowsSystem):
            logger.info(f"{_('Restarting explorer.exe')} ...")
            System.restart_explorer()
            progress_callback(100.0)


__all__ = [
    "WinRestartExplorerCommand",
]
