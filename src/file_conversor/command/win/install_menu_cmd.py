
# src\file_conversor\command\win\install_menu_cmd.py

from enum import StrEnum
from typing import override

# user-provided modules
from file_conversor.backend.win_reg_backend import WinRegBackend
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.config import (
    Configuration,
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


WinInstallMenuExternalDependencies = WinRegBackend.EXTERNAL_DEPENDENCIES


class WinInstallMenuInFormats(StrEnum):
    """ empty enum since this command does not process files, but is just a system command to restart explorer.exe """


class WinInstallMenuOutFormats(StrEnum):
    """ empty enum since this command does not process files, but is just a system command to restart explorer.exe """


class WinInstallMenuCommand(AbstractCommand[WinInstallMenuInFormats, WinInstallMenuOutFormats]):
    reboot_explorer: bool

    @classmethod
    @override
    def _external_dependencies(cls):
        return WinInstallMenuExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return WinInstallMenuInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return WinInstallMenuOutFormats

    @override
    def execute(self):
        step_completion = 40.0  # percentage of total progress allocated to each of the uninstall/install steps (total 80% for both)

        winreg_backend = WinRegBackend(verbose=STATE.loglevel.get().is_verbose())

        ctx_menu = WinContextMenu.get_instance()
        reg_file = ctx_menu.get_reg_file()

        logger.info(f"{_('Uninstalling app context menu in Windows Explorer')} ...")
        winreg_backend.delete_keys(
            reg_file,
            progress_callback=lambda p: self.progress_callback(p * step_completion / 100.0),  # Scale progress to 40% for uninstalling
        )

        logger.info(f"{_('Installing app context menu in Windows Explorer')} ...")
        winreg_backend.import_file(
            reg_file,
            progress_callback=lambda p: self.progress_callback(step_completion + p * step_completion / 100.0),  # Scale progress to 80% for installing
        )

        if self.reboot_explorer and isinstance(System, WindowsSystem):
            System.restart_explorer()
        else:
            logger.warning(_("Restart explorer.exe or log off from Windows, to make changes effective immediately."))

        logger.info(f"{_('Context Menu Install')}: [bold green]{_('SUCCESS')}[/].")
        self.progress_callback(100.0)


__all__ = [
    "WinInstallMenuExternalDependencies",
    "WinInstallMenuInFormats",
    "WinInstallMenuOutFormats",
    "WinInstallMenuCommand",
]
