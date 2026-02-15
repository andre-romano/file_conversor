# src\file_conversor\cli\ppt\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils.abstract_typer_group import AbstractTyperGroup

from file_conversor.cli.ppt.convert_cli import PptConvertCLI

from file_conversor.config.locale import get_translation

_ = get_translation()


class PptTyperGroup(AbstractTyperGroup):
    class Panels(Enum):
        NONE = None

    class Commands(Enum):
        CONVERT = "convert"

    def __init__(self, group_name: str, rich_help_panel: str) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            help=f"{_('Presentation file manipulation')} {_('(requires LibreOffice)')})",
        )

        # add subcommands
        self.add(
            PptConvertCLI(
                group_name=group_name,
                command_name=self.Commands.CONVERT.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
        )


__all__ = [
    "PptTyperGroup",
]
