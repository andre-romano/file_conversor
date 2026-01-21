
# src\file_conversor\cli\audio\convert_cmd.py

from typing import Annotated, Iterable, List
from pathlib import Path

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import AudioBitrateOption, FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.cli.audio._ffmpeg_cmd import ffmpeg_audio_run

from file_conversor.backend import FFmpegBackend

from file_conversor.config import Environment, Configuration, Log, get_translation

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AudioConvertCommand(AbstractTyperCommand):
    """Audio convert command class."""

    EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # FFMPEG commands
        icons_folder_path = Environment.get_icons_folder()
        for ext in FFmpegBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="to_m4a",
                    description="To M4A",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f m4a "%1""',
                    icon=str(icons_folder_path / 'm4a.ico'),
                ),
                WinContextCommand(
                    name="to_mp3",
                    description="To MP3",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f mp3 "%1""',
                    icon=str(icons_folder_path / 'mp3.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=_('Convert a audio/video file to an audio format.'),
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.webm -f mp3 -od output_dir/ --audio-bitrate 192`
    - `file_conversor {group_name} {command_name} input_file.mp3 -f m4a`
""",
        )

    def convert(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(FFmpegBackend.SUPPORTED_IN_FORMATS)],
        file_format: Annotated[str, FormatOption(FFmpegBackend.SUPPORTED_OUT_AUDIO_FORMATS)],
        audio_bitrate: Annotated[int, AudioBitrateOption()] = CONFIG.audio_bitrate,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        ffmpeg_audio_run(
            input_files,
            file_format=file_format,
            audio_bitrate=audio_bitrate,
            output_dir=output_dir,
        )


__all__ = [
    "AudioConvertCommand",
    "ffmpeg_audio_run",
]
