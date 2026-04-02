
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
from file_conversor.config import Log, State, get_translation
from file_conversor.system import ContextMenu, ContextMenuItem


# get app config
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AudioInfoCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        # FFMPEG commands
        for ext_in in AudioInfoCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="info",
                    description="Get Info",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / 'info.ico',
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
        input_files: Annotated[list[Path], InputFilesArgument(AudioInfoCommand.get_in_formats())],
    ):
        VideoInfoCLI(
            group_name=self.GROUP_NAME,
            command_name=self.COMMAND_NAME,
            rich_help_panel=None,
        ).info(
            input_files=input_files,
        )


__all__ = [
    "AudioInfoCLI",
]
