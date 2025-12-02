
# src\file_conversor\cli\text\check_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print


# user-provided modules
from file_conversor.backend import TextBackend

from file_conversor.cli.text._typer import COMMAND_NAME, CHECK_NAME
from file_conversor.config import Environment, Configuration, State, Log, get_translation

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

EXTERNAL_DEPENDENCIES = TextBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    for ext in TextBackend.SUPPORTED_IN_FORMATS:
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


def execute_text_check_cmd(
    input_files: List[Path],
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    text_backend = TextBackend(verbose=STATE["verbose"])
    logger.info(f"{_('Checking files')} ...")

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        text_backend.check(
            input_file=input_file,
        )
        progress_callback(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=Path(), overwrite=True)  # overwrite is True because no output files are generated
    cmd_mgr.run(callback)

    logger.info(f"{_('Check')}: [bold green]{_('SUCCESS')}[/].")


# text check
@typer_cmd.command(
    name=CHECK_NAME,
    help=f"""
        {_('Checks a text file schema compliance (json, xml, yaml, etc).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor {COMMAND_NAME} {CHECK_NAME} file.json` 

- `file_conversor {COMMAND_NAME} {CHECK_NAME} file1.json file2.yaml` 
""")
def check(
    input_files: Annotated[List[Path], InputFilesArgument(TextBackend)],
):
    execute_text_check_cmd(
        input_files=input_files,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_text_check_cmd",
]
