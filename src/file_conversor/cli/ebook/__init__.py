
# src\file_conversor\cli\ebook\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils import AbstractTyperGroup
from file_conversor.cli.ebook.convert_cli import EbookConvertCLI
from file_conversor.config.locale import get_translation


_ = get_translation()


class EbookTyperGroup(AbstractTyperGroup):
    class Panels(Enum):
        NONE = None

    class Commands(Enum):
        CONVERT = "convert"

    def __init__(self, group_name: str, rich_help_panel: str) -> None:
        super().__init__(
            group_name=group_name,
            help=_("Ebook file manipulation (requires Calibre external library)"),
            rich_help_panel=rich_help_panel,
        )

        # add subcommands
        self.add(
            EbookConvertCLI(
                group_name=group_name,
                command_name=self.Commands.CONVERT.value,
                rich_help_panel=rich_help_panel,
            ),
        )


__all__ = [
    "EbookTyperGroup",
]
