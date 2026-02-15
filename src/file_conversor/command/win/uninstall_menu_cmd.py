
# src\file_conversor\command\win\uninstall_menu_cmd.py

from enum import Enum
from typing import Any, Callable

# user-provided modules
from file_conversor.backend.win_reg_backend import WinRegBackend
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win import WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WinUninstallMenuCommand:
    EXTERNAL_DEPENDENCIES = WinRegBackend.EXTERNAL_DEPENDENCIES

    class SupportedInFormats(Enum):
        """ empty enum since this command does not process files, but is just a system command to restart explorer.exe """
    class SupportedOutFormats(Enum):
        """ empty enum since this command does not process files, but is just a system command to restart explorer.exe """

    @classmethod
    def uninstall_menu(
        cls,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        winreg_backend = WinRegBackend(verbose=STATE.loglevel.get().is_verbose())
        ctx_menu = WinContextMenu.get_instance(icons_folder=Environment.get_icons_folder())

        logger.info(f"{_('Removing app context menu from Windows Explorer')} ...")
        winreg_backend.delete_keys(
            ctx_menu.get_reg_file(),
            progress_callback=progress_callback,
        )

        logger.info(f"{_('Context Menu Uninstall')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "WinUninstallMenuCommand",
]
