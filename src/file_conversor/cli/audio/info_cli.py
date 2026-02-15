
# src\file_conversor\cli\audio\info_cli.py

from pathlib import Path
from typing import Annotated, override

# CLI
from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import InputFilesArgument
from file_conversor.cli.video.info_cli import VideoInfoCLI

# COMMAND
from file_conversor.command.audio import AudioInfoCommand

# CORE
from file_conversor.config import Environment, Log, State, get_translation
from file_conversor.system.win import WinContextCommand, WinContextMenu


# get app config
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AudioInfoCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = AudioInfoCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # FFMPEG commands
        icons_folder_path = Environment.get_icons_folder()
        for mode in AudioInfoCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="info",
                    description="Get Info",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / 'info.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Audio info command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.info,
            help=f"""
    {_('Get information about an audio file.')}

    {_('This command retrieves metadata and other information about the audio file')}:

    - {_('Format')} (mp3, m4a, etc)

    - {_('Duration')} (HH:MM:SS)

    - {_('Other properties')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} filename.m4a`

    - `file_conversor {group_name} {command_name} other_filename.mp3`
""",
        )

    def info(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in AudioInfoCommand.SupportedInFormats)],
    ):
        VideoInfoCLI("", "", None).info(input_files)  # reuse video info logic


__all__ = [
    "AudioInfoCLI",
]
