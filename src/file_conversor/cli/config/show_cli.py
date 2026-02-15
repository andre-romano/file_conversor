
# src\file_conversor\cli\config\show_cli.py

from typing import override

from rich import print
from rich.pretty import Pretty

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.command.config import ConfigShowCommand
from file_conversor.config import Configuration, Log, get_translation
from file_conversor.system.win.ctx_menu import WinContextMenu


# app configuration
CONFIG = Configuration.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# create command


class ConfigShowCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = ConfigShowCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # no context menu for this command

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config show command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.show,
            help=_('Show the current configuration of the application'),
            epilog=f"""
    **{_('Examples')}:** 

        - `file_conversor {group_name} {command_name}`
    """)

    def show(self):
        ConfigShowCommand.show()
        print(f"{_('Configuration')}:", Pretty(CONFIG.to_dict(), expand_all=True))


__all__ = [
    "ConfigShowCLI",
]
