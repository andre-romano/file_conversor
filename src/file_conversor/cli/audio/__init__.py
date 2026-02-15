
# src\file_conversor\cli\audio\__init__.py

from enum import Enum

from file_conversor.cli._utils import AbstractTyperGroup
from file_conversor.cli.audio.check_cli import AudioCheckCLI
from file_conversor.cli.audio.convert_cli import AudioConvertCLI
from file_conversor.cli.audio.info_cli import AudioInfoCLI
from file_conversor.config.locale import get_translation


_ = get_translation()


class AudioTyperGroup(AbstractTyperGroup):
    """Audio group command class."""

    class Panels(Enum):
        NONE = None

    class Commands(Enum):
        CHECK = "check"
        CONVERT = "convert"
        INFO = "info"

    def __init__(self, group_name: str, rich_help_panel: str) -> None:
        super().__init__(
            group_name=group_name,
            help=_("Audio file manipulation (requires FFMpeg external library)"),
            rich_help_panel=rich_help_panel,
        )

        # add subcommands
        self.add(
            AudioConvertCLI(
                group_name=group_name,
                command_name=self.Commands.CONVERT.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
            AudioInfoCLI(
                group_name=group_name,
                command_name=self.Commands.INFO.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
            AudioCheckCLI(
                group_name=group_name,
                command_name=self.Commands.CHECK.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
        )


__all__ = [
    "AudioTyperGroup",
]
