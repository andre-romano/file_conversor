# src\file_conversor\cli\text\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils.abstract_typer_group import AbstractTyperGroup

from file_conversor.cli.text.check_cmd import TextCheckTyperCommand
from file_conversor.cli.text.compress_cmd import TextCompressTyperCommand
from file_conversor.cli.text.convert_cmd import TextConvertTyperCommand

from file_conversor.config.locale import get_translation

_ = get_translation()


class TextTyperGroup(AbstractTyperGroup):
    class Panels(Enum):
        NONE = None

    class Commands(Enum):
        CHECK = "check"
        COMPRESS = "compress"
        CONVERT = "convert"

    def __init__(self, group_name: str, rich_help_panel: str) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            help=_("Text file manipulation (json, xml, etc)"),
        )

        # add subcommands
        self.add(
            TextCheckTyperCommand(
                group_name=group_name,
                command_name=self.Commands.CHECK.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
            TextCompressTyperCommand(
                group_name=group_name,
                command_name=self.Commands.COMPRESS.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
            TextConvertTyperCommand(
                group_name=group_name,
                command_name=self.Commands.CONVERT.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
        )


__all__ = [
    "TextTyperGroup",
]
