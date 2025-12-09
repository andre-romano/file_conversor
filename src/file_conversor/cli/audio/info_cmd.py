
# src\file_conversor\cli\audio\info_cmd.py

import typer

from rich import print

from typing import Annotated, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFprobeBackend
from file_conversor.cli.audio._typer import COMMAND_NAME, INFO_NAME

from file_conversor.cli.video.info_cmd import info as info_video_cmd, EXTERNAL_DEPENDENCIES

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils.typer_utils import InputFilesArgument

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    # FFMPEG commands
    icons_folder_path = Environment.get_icons_folder()
    for ext in FFprobeBackend.SUPPORTED_IN_AUDIO_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="info",
                description="Get Info",
                command=f'cmd.exe /k "{Environment.get_executable()} "{COMMAND_NAME}" "{INFO_NAME}" "%1""',
                icon=str(icons_folder_path / 'info.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=INFO_NAME,
    help=f"""
        {_('Get information about a audio file.')}

        {_('This command retrieves metadata and other information about the audio file')}:

        - {_('Format')} (mp3, m4a, etc)

        - {_('Duration')} (HH:MM:SS)

        - {_('Other properties')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {INFO_NAME} filename.m4a`

        - `file_conversor {COMMAND_NAME} {INFO_NAME} other_filename.mp3`
    """)
def info(
    input_files: Annotated[List[Path], InputFilesArgument(FFprobeBackend.SUPPORTED_IN_AUDIO_FORMATS)],
):
    info_video_cmd(input_files)


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
