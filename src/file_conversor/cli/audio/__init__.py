
# src\file_conversor\cli\audio\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils import AbstractTyperGroup

from file_conversor.cli.audio.check_cmd import AudioCheckCommand
from file_conversor.cli.audio.convert_cmd import AudioConvertCommand
from file_conversor.cli.audio.info_cmd import AudioInfoCommand

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
            AudioConvertCommand(
                group_name=group_name,
                command_name=self.Commands.CONVERT.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
            AudioInfoCommand(
                group_name=group_name,
                command_name=self.Commands.INFO.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
            AudioCheckCommand(
                group_name=group_name,
                command_name=self.Commands.CHECK.value,
                rich_help_panel=self.Panels.NONE.value,
            ),
        )


__all__ = [
    "AudioTyperGroup",
]
