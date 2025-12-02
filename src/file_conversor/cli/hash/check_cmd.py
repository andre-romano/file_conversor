
# src\file_conversor\cli\hash\check_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend import HashBackend

from file_conversor.cli.hash._typer import COMMAND_NAME, CHECK_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.typer_utils import InputFilesArgument

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = HashBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    for ext in HashBackend.SUPPORTED_IN_FORMATS:
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


def execute_hash_check_cmd(
    input_files: List[Path],
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    hash_backend = HashBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"{_('Checking file')} '{input_file}' ...")
        hash_backend.check(
            input_file=input_file,
            progress_callback=lambda p: progress_callback(progress_mgr.update_progress(p)),
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=Path(), overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback)

    logger.info(f"{_('Hash check')}: [bold green]{_('SUCCESS')}[/].")


@typer_cmd.command(
    name=CHECK_NAME,
    help=f"""
        {_('Checks a hash file (.sha256, .sha1, etc).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor {COMMAND_NAME} {CHECK_NAME} file.sha256` 
- `file_conversor {COMMAND_NAME} {CHECK_NAME} file.sha1 file.sha3_512` 
""")
def check(
    input_files: Annotated[List[Path], InputFilesArgument(HashBackend)],
):
    execute_hash_check_cmd(
        input_files=input_files,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_hash_check_cmd",
]
