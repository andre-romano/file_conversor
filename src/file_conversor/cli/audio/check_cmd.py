
# src\file_conversor\cli\audio\check_cmd.py

import typer

from rich import print

from typing import Annotated, Any, Callable, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFprobeBackend

from file_conversor.cli.audio._typer import COMMAND_NAME, CHECK_NAME

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
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
    for ext in FFprobeBackend.SUPPORTED_IN_AUDIO_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="check",
                description="Check",
                command=f'cmd.exe /k "{Environment.get_executable()} "{COMMAND_NAME}" "{CHECK_NAME}" "%1""',
                icon=str(icons_folder_path / 'check.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_audio_check_cmd(
    input_files: List[Path],
    progress_callback: Callable[[float], Any] = lambda p: p,
) -> None:
    """Execute audio check command."""
    # init backend
    backend = FFprobeBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        # display current progress
        parser = FFprobeParser(backend, input_file)
        parser.run()
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=Path(), overwrite=True)  # overwrite is True because no output files are generated
    cmd_mgr.run(callback)

    logger.info(f"{_('FFMpeg check')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


@typer_cmd.command(
    name=CHECK_NAME,
    help=f"""
        {_('Checks audio files for corruption / inconsistencies.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {CHECK_NAME} input_file.mp3`
    """)
def check(
    input_files: Annotated[List[Path], InputFilesArgument(FFprobeBackend.SUPPORTED_IN_AUDIO_FORMATS)],
):
    execute_audio_check_cmd(input_files)


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_audio_check_cmd",
]
