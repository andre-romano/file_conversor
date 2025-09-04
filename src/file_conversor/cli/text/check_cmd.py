
# src\file_conversor\cli\text\check_cmd.py

import typer

from pathlib import Path
from typing import Annotated, List

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
                command=f'cmd /k "{Environment.get_executable()} "{COMMAND_NAME}" "{CHECK_NAME}" "%1""',
                icon=str(icons_folder_path / 'check.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


# text check
@typer_cmd.command(
    name=CHECK_NAME,
    help=f"""
        {_('Checks a text file (json, xml, yaml, etc).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor {COMMAND_NAME} {CHECK_NAME} file.json` 

- `file_conversor {COMMAND_NAME} {CHECK_NAME} file1.json file2.yaml` 
""")
def check(
    input_files: Annotated[List[str], InputFilesArgument(TextBackend)],
):
    text_backend = TextBackend(verbose=STATE["verbose"])
    logger.info(f"{_('Checking files')} ...")

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        text_backend.check(
            input_file=input_file,
        )
    cmd_mgr = CommandManager(input_files, output_dir=Path(), overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback)
    logger.info(f"{_('Check')}: [bold green]{_('SUCCESS')}[/].")
