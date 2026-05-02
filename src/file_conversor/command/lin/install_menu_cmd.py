# src/file_conversor/command/lin/install_menu_cmd.py

from enum import StrEnum
from typing import override

from file_conversor.backend.lin_desktop_backend import LinDesktopBackend
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.config import LOG, get_translation
from file_conversor.system.lin import LinuxContextMenu


_ = get_translation()
logger = LOG.getLogger(__name__)


LinInstallMenuExternalDependencies: set[str] = set()


class LinInstallMenuInFormats(StrEnum):
    """Empty enum since this command is a system command, not a file-conversion command."""


class LinInstallMenuOutFormats(StrEnum):
    """Empty enum since this command is a system command, not a file-conversion command."""


class LinInstallMenuCommand(AbstractCommand[LinInstallMenuInFormats, LinInstallMenuOutFormats]):
    rebuild_cache: bool

    @classmethod
    @override
    def _external_dependencies(cls):
        return LinInstallMenuExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return LinInstallMenuInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return LinInstallMenuOutFormats

    @override
    def execute(self) -> None:
        step_completion = 40.0  # percentage allocated to each uninstall/install step (80% total)

        backend = LinDesktopBackend()
        ctx_menu = LinuxContextMenu.get_instance()

        logger.info(f"{_('Uninstalling app context menu in Dolphin')} ...")
        backend.uninstall(
            ctx_menu.get_desktop_uninstall_paths(),
            progress_callback=lambda p: self.progress_callback(p * step_completion / 100.0),
        )

        logger.info(f"{_('Installing app context menu in Dolphin')} ...")
        backend.install(
            ctx_menu.get_desktop_files(),
            progress_callback=lambda p: self.progress_callback(step_completion + p * step_completion / 100.0),
        )

        if self.rebuild_cache:
            logger.info(f"{_('Rebuilding KDE service cache')} ...")
            backend.rebuild_cache(
                progress_callback=lambda p: self.progress_callback(80.0 + p * 20.0 / 100.0),
            )
        else:
            logger.warning(_("Run 'kbuildsycoca6' or log off from KDE to make context menu changes effective immediately."))

        logger.info(f"{_('Context Menu Install')}: [bold green]{_('SUCCESS')}[/].")
        self.progress_callback(100.0)


__all__ = [
    "LinInstallMenuExternalDependencies",
    "LinInstallMenuInFormats",
    "LinInstallMenuOutFormats",
    "LinInstallMenuCommand",
]
