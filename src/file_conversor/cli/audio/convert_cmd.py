
# src\file_conversor\cli\audio\convert_cmd.py

import typer

from rich import print

from typing import Annotated, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend

from file_conversor.cli.audio._ffmpeg_cmd import ffmpeg_audio_run
from file_conversor.cli.audio._typer import COMMAND_NAME, CONVERT_NAME

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.validators import check_valid_options
from file_conversor.utils.typer_utils import AudioBitrateOption, AudioCodecOption, FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    # FFMPEG commands
    icons_folder_path = Environment.get_icons_folder()
    for ext in FFmpegBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_m4a",
                description="To M4A",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" -f m4a "%1""',
                icon=str(icons_folder_path / 'm4a.ico'),
            ),
            WinContextCommand(
                name="to_mp3",
                description="To MP3",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" -f mp3 "%1""',
                icon=str(icons_folder_path / 'mp3.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=CONVERT_NAME,
    help=f"""
        {_('Convert a audio/video file to an audio format.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.webm -f mp3 -od output_dir/ --audio-bitrate 192`
        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.mp3 -f m4a`
    """)
def convert_audio(
    input_files: Annotated[List[Path], InputFilesArgument(FFmpegBackend.SUPPORTED_IN_FORMATS)],

    file_format: Annotated[str, FormatOption(FFmpegBackend.SUPPORTED_OUT_AUDIO_FORMATS)],

    audio_bitrate: Annotated[int, AudioBitrateOption()] = CONFIG["audio-bitrate"],

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    ffmpeg_audio_run(
        input_files,
        file_format=file_format,
        audio_bitrate=audio_bitrate,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "ffmpeg_audio_run",
]
