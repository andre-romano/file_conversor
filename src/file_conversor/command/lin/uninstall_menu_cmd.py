# src/file_conversor/command/lin/uninstall_menu_cmd.py

from enum import StrEnum
from typing import override

from file_conversor.backend.lin_desktop_backend import LinDesktopBackend
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.config import LOG, get_translation
from file_conversor.system.lin import LinuxContextMenu


_ = get_translation()
logger = LOG.getLogger(__name__)


LinUninstallMenuExternalDependencies: set[str] = set()


class LinUninstallMenuInFormats(StrEnum):
    """Empty enum since this command is a system command, not a file-conversion command."""


class LinUninstallMenuOutFormats(StrEnum):
    """Empty enum since this command is a system command, not a file-conversion command."""


class LinUninstallMenuCommand(AbstractCommand[LinUninstallMenuInFormats, LinUninstallMenuOutFormats]):
    @classmethod
    @override
    def _external_dependencies(cls):
        return LinUninstallMenuExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return LinUninstallMenuInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return LinUninstallMenuOutFormats

    @override
    def execute(self) -> None:
        backend = LinDesktopBackend()
        ctx_menu = LinuxContextMenu.get_instance()

        logger.info(f"{_('Removing app context menu from Dolphin')} ...")
        backend.uninstall(
            ctx_menu.get_desktop_uninstall_paths(),
            progress_callback=self.progress_callback,
        )

        logger.info(f"{_('Context Menu Uninstall')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "LinUninstallMenuExternalDependencies",
    "LinUninstallMenuInFormats",
    "LinUninstallMenuOutFormats",
    "LinUninstallMenuCommand",
]
