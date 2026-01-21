
# src\file_conversor\cli\audio\info_cmd.py

from typing import Annotated, Iterable, List
from pathlib import Path

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import InputFilesArgument

from file_conversor.cli.video.info_cmd import VideoInfoTyperCommand, FFprobeBackend

from file_conversor.config import Environment, Log, get_translation

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AudioInfoCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = FFprobeBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # FFMPEG commands
        icons_folder_path = Environment.get_icons_folder()
        for ext in FFprobeBackend.SUPPORTED_IN_AUDIO_FORMATS:
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
    {_('Get information about a audio file.')}

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
        input_files: Annotated[List[Path], InputFilesArgument(FFprobeBackend.SUPPORTED_IN_AUDIO_FORMATS)],
    ):
        typer_cmd = VideoInfoTyperCommand("dummy", "dummy", None)
        typer_cmd.info(input_files)


__all__ = [
    "AudioInfoCommand",
]
