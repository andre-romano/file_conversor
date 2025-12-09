
# src\file_conversor\cli\video\info_cmd.py

import typer

from rich import print

from typing import Annotated, List
from datetime import timedelta
from pathlib import Path

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.console import Group

# user-provided modules
from file_conversor.backend import FFprobeBackend

from file_conversor.cli.video._typer import OTHERS_PANEL as RICH_HELP_PANEL
from file_conversor.cli.video._typer import COMMAND_NAME, INFO_NAME

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils.backend import FFprobeParser
from file_conversor.utils.typer_utils import InputFilesArgument

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = FFprobeBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    # FFMPEG commands
    icons_folder_path = Environment.get_icons_folder()
    for ext in FFprobeBackend.SUPPORTED_IN_VIDEO_FORMATS:
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
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Get information about a video file.')}

        {_('This command retrieves metadata and other information about the video file')}:

        - {_('Format')} (avi, mp4, mov, etc)

        - {_('Duration')} (HH:MM:SS)

        - {_('Other properties')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {INFO_NAME} filename.webm`

        - `file_conversor {COMMAND_NAME} {INFO_NAME} other_filename.mp4`
    """)
def info(
    input_files: Annotated[List[Path], InputFilesArgument(FFprobeBackend)],
):

    ffprobe_backend = FFprobeBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )
    for filename in input_files:
        logger.info(f"{_('Parsing file metadata for')} '{filename}' ...")
        try:
            parser = FFprobeParser(ffprobe_backend, filename)
            parser.run()
            # Agrupar e exibir tudo com Rich
            group = Group(*[
                *parser.get_format().rich(),
                *parser.get_streams().rich(),
                *parser.get_chapters().rich(),
            ])
            print(Panel(group, title=f"🧾 {_('File Analysis')}", border_style="blue"))
        except Exception as e:
            logger.error(f"{_('Error parsing file')} '{filename}': {e}")
            continue


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
