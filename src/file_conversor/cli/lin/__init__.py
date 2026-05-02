# src/file_conversor/cli/lin/__init__.py

from enum import Enum

from file_conversor.cli._utils.abstract_typer_group import AbstractTyperGroup
from file_conversor.cli.lin.install_menu_cli import LinInstallMenuCLI
from file_conversor.cli.lin.uninstall_menu_cli import LinUninstallMenuCLI
from file_conversor.config.locale import get_translation


_ = get_translation()


class LinTyperGroup(AbstractTyperGroup):
    class Panels(Enum):
        CONTEXT_MENU = _("Context menu")

    class Commands(Enum):
        INSTALL_MENU = "install-menu"
        UNINSTALL_MENU = "uninstall-menu"

    def __init__(self, group_name: str, rich_help_panel: str, hidden: bool) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            help=_("Linux OS commands (for Linux ONLY)"),
            hidden=hidden,
        )

        self.add(
            LinInstallMenuCLI(
                group_name=group_name,
                command_name=self.Commands.INSTALL_MENU.value,
                rich_help_panel=self.Panels.CONTEXT_MENU.value,
            ),
            LinUninstallMenuCLI(
                group_name=group_name,
                command_name=self.Commands.UNINSTALL_MENU.value,
                rich_help_panel=self.Panels.CONTEXT_MENU.value,
            ),
        )
