
# src\file_conversor\command\win\install_menu_cmd.py

from enum import Enum
from typing import Any, Callable

# user-provided modules
from file_conversor.backend.win_reg_backend import WinRegBackend
from file_conversor.command.video._ffmpeg_cmd_helper import FFmpegCmdHelper
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system import System, WinContextMenu, WindowsSystem


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WinInstallMenuCommand:
    EXTERNAL_DEPENDENCIES = WinRegBackend.EXTERNAL_DEPENDENCIES

    class SupportedInFormats(Enum):
        """ empty enum since this command does not process files, but is just a system command to restart explorer.exe """
    class SupportedOutFormats(Enum):
        """ empty enum since this command does not process files, but is just a system command to restart explorer.exe """

    VideoProfile = FFmpegCmdHelper.VideoProfile
    VideoEncoding = FFmpegCmdHelper.VideoEncoding
    VideoQuality = FFmpegCmdHelper.VideoQuality

    @classmethod
    def install_menu(
        cls,
        reboot_explorer: bool,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        step_completion = 40.0  # percentage of total progress allocated to each of the uninstall/install steps (total 80% for both)

        winreg_backend = WinRegBackend(verbose=STATE.loglevel.get().is_verbose())

        ctx_menu = WinContextMenu.get_instance(icons_folder=Environment.get_icons_folder())
        reg_file = ctx_menu.get_reg_file()

        logger.info(f"{_('Uninstalling app context menu in Windows Explorer')} ...")
        winreg_backend.delete_keys(
            reg_file,
            progress_callback=lambda p: progress_callback(p * step_completion / 100.0),  # Scale progress to 40% for uninstalling
        )

        logger.info(f"{_('Installing app context menu in Windows Explorer')} ...")
        winreg_backend.import_file(
            reg_file,
            progress_callback=lambda p: progress_callback(step_completion + p * step_completion / 100.0),  # Scale progress to 80% for installing
        )

        if reboot_explorer and isinstance(System, WindowsSystem):
            System.restart_explorer()
        else:
            logger.warning(_("Restart explorer.exe or log off from Windows, to make changes effective immediately."))

        logger.info(f"{_('Context Menu Install')}: [bold green]{_('SUCCESS')}[/].")
        progress_callback(100.0)


__all__ = [
    "WinInstallMenuCommand",
]
