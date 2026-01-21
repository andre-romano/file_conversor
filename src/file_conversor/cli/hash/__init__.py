# src\file_conversor\cli\hash\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils import AbstractTyperGroup
from file_conversor.config.locale import get_translation

from file_conversor.cli.hash.check_cmd import HashCheckCommand
from file_conversor.cli.hash.create_cmd import HashCreateCommand

_ = get_translation()


class HashTyperGroup(AbstractTyperGroup):
    """Config group command class."""

    class Panels(Enum):
        NONE = None

    class Commands(Enum):
        CHECK = "check"
        CREATE = "create"

    def __init__(self, group_name: str, rich_help_panel: str) -> None:
        super().__init__(
            group_name=group_name,
            help=_("Hashing manipulation (check, gen, etc)"),
            rich_help_panel=rich_help_panel,
        )

        # add subcommands
        self.add(
            HashCheckCommand(
                group_name=group_name,
                command_name=self.Commands.CHECK.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
            HashCreateCommand(
                group_name=group_name,
                command_name=self.Commands.CREATE.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
        )


__all__ = [
    "HashTyperGroup",
]
