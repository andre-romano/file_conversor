# src\file_conversor\cli\win\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils.abstract_typer_group import AbstractTyperGroup

# CLI
from file_conversor.cli.win.install_menu_cli import WinInstallMenuCLI
from file_conversor.cli.win.restart_explorer_cli import WinRestartExplorerCLI
from file_conversor.cli.win.uninstall_menu_cli import WinUninstallMenuCLI

# CORE
from file_conversor.config.locale import get_translation


_ = get_translation()


class WinTyperGroup(AbstractTyperGroup):
    class Panels(Enum):
        CONTEXT_MENU = _("Context menu")
        OTHERS = _("Other commands")

    class Commands(Enum):
        INSTALL_MENU = "install-menu"
        UNINSTALL_MENU = "uninstall-menu"
        RESTART_EXPLORER = "restart-explorer"

    def __init__(self, group_name: str, rich_help_panel: str, hidden: bool) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            help=_("Windows OS commands (for Windows ONLY)"),
            hidden=hidden,
        )

        # add subcommands
        self.add(
            # OTHERS_PANEL
            WinRestartExplorerCLI(
                group_name=group_name,
                command_name=self.Commands.RESTART_EXPLORER.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),

            # CONTEXT_MENU_PANEL
            WinInstallMenuCLI(
                group_name=group_name,
                command_name=self.Commands.INSTALL_MENU.value,
                rich_help_panel=self.Panels.CONTEXT_MENU.value,
            ),
            WinUninstallMenuCLI(
                group_name=group_name,
                command_name=self.Commands.UNINSTALL_MENU.value,
                rich_help_panel=self.Panels.CONTEXT_MENU.value,
            ),
        )


__all__ = [
    "WinTyperGroup",
]
