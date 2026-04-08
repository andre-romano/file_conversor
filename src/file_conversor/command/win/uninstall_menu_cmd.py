
# src\file_conversor\command\win\uninstall_menu_cmd.py

from enum import StrEnum
from typing import override

# user-provided modules
from file_conversor.backend.win_reg_backend import WinRegBackend
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.config import LOG, STATE, get_translation
from file_conversor.system.win import WinContextMenu


_ = get_translation()
logger = LOG.getLogger(__name__)

WinUninstallMenuExternalDependencies = WinRegBackend.EXTERNAL_DEPENDENCIES


class WinUninstallMenuInFormats(StrEnum):
    """ empty enum since this command does not process files, but is just a system command to restart explorer.exe """


class WinUninstallMenuOutFormats(StrEnum):
    """ empty enum since this command does not process files, but is just a system command to restart explorer.exe """


class WinUninstallMenuCommand(AbstractCommand[WinUninstallMenuInFormats, WinUninstallMenuOutFormats]):
    @classmethod
    @override
    def _external_dependencies(cls):
        return WinUninstallMenuExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return WinUninstallMenuInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return WinUninstallMenuOutFormats

    @override
    def execute(self):
        winreg_backend = WinRegBackend(verbose=STATE.loglevel.get().is_verbose())
        ctx_menu = WinContextMenu.get_instance()

        logger.info(f"{_('Removing app context menu from Windows Explorer')} ...")
        winreg_backend.delete_keys(
            ctx_menu.get_reg_file(),
            progress_callback=self.progress_callback,
        )

        logger.info(f"{_('Context Menu Uninstall')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "WinUninstallMenuExternalDependencies",
    "WinUninstallMenuInFormats",
    "WinUninstallMenuOutFormats",
    "WinUninstallMenuCommand",
]
