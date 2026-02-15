# src\file_conversor\cli\doc\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils import AbstractTyperGroup
from file_conversor.cli.doc.convert_cli import DocConvertCLI
from file_conversor.config.locale import get_translation


_ = get_translation()


class DocTyperGroup(AbstractTyperGroup):
    """Config group command class."""
    class Panels(Enum):
        NONE = None

    class Commands(Enum):
        CONVERT = "convert"

    def __init__(self, group_name: str, rich_help_panel: str) -> None:
        super().__init__(
            group_name=group_name,
            help=f"{_('Document file manipulation')} {_('(requires LibreOffice)')})",
            rich_help_panel=rich_help_panel,
        )

        # add subcommands
        self.add(
            DocConvertCLI(
                group_name=group_name,
                command_name=self.Commands.CONVERT.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
        )


__all__ = [
    "DocTyperGroup",
]
