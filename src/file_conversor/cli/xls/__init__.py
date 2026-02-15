# src\file_conversor\cli\xls\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils import AbstractTyperGroup

# CLI
from file_conversor.cli.xls.convert_cli import XlsConvertCLI

# CORE
from file_conversor.config.locale import get_translation


_ = get_translation()


class XlsTyperGroup(AbstractTyperGroup):
    class Panels(Enum):
        NONE = None

    class Commands(Enum):
        CONVERT = "convert"

    def __init__(self, group_name: str, rich_help_panel: str) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            help=f"{_('Spreadsheet file manipulation')} {_('(requires LibreOffice)')})",
        )

        # add subcommands
        self.add(
            XlsConvertCLI(
                group_name=group_name,
                command_name=self.Commands.CONVERT.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
        )


__all__ = [
    "XlsTyperGroup",
]
