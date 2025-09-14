
# src\file_conversor\cli\video\check_cmd.py

import subprocess
import typer

from rich import print

from typing import Annotated, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend

from file_conversor.cli.video._typer import OTHERS_PANEL as RICH_HELP_PANEL
from file_conversor.cli.video._typer import COMMAND_NAME, CHECK_NAME
from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument

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
    for ext in FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="check",
                description="Check",
                command=f'cmd /k "{Environment.get_executable()} "{COMMAND_NAME}" "{CHECK_NAME}" "%1""',
                icon=str(icons_folder_path / 'check.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=CHECK_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Checks a audio/video file for corruption / inconsistencies.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {CHECK_NAME} input_file.webm`
    """)
def check(
    input_files: Annotated[List[Path], InputFilesArgument(FFmpegBackend)],
):
    # init ffmpeg
    ffmpeg_backend = FFmpegBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
        overwrite_output=STATE["overwrite-output"],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        # display current progress
        ffmpeg_backend.set_files(input_file=input_file, output_file="-")
        try:
            ffmpeg_backend.execute(
                progress_callback=progress_mgr.update_progress
            )
        except subprocess.CalledProcessError:
            logger.error(f"{_('FFMpeg check')}: [red][bold]{_('FAILED')}[/bold][/red]")
            raise RuntimeError(f"{_('File')} '{input_file}' {_('is corrupted or has inconsistencies')}")
        progress_mgr.complete_step()

    cmd_mgr = CommandManager(input_files, output_dir=Path(), overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_suffix=f".{format}")

    logger.info(f"{_('FFMpeg check')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
