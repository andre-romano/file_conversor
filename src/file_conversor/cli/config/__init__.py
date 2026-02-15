
# src\file_conversor\cli\config\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils.abstract_typer_group import AbstractTyperGroup
from file_conversor.cli.config.set_cli import ConfigSetCLI
from file_conversor.cli.config.show_cli import ConfigShowCLI
from file_conversor.config.locale import get_translation


_ = get_translation()


class ConfigTyperGroup(AbstractTyperGroup):
    """Config group command class."""
    class Panels(Enum):
        NONE = None

    class Commands(Enum):
        SHOW = "show"
        SET = "set"

    def __init__(self, group_name: str, rich_help_panel: str) -> None:
        super().__init__(
            group_name=group_name,
            help=_("Configure default options"),
            rich_help_panel=rich_help_panel,
        )

        # add subcommands
        self.add(
            ConfigShowCLI(
                group_name=group_name,
                command_name=self.Commands.SHOW.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
            ConfigSetCLI(
                group_name=group_name,
                command_name=self.Commands.SET.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
        )


__all__ = [
    "ConfigTyperGroup",
]
