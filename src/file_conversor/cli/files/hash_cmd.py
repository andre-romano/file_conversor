
# src\file_conversor\cli\utils\hash_cmd.py

import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend import HashBackend

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

from file_conversor.utils.progress_manager import ProgressManager
from file_conversor.utils.validators import *
from file_conversor.utils.typer import *

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

hash_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    for ext in HashBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="check",
                description="Check",
                command=f'cmd /k "{Environment.get_executable()} hash check "%1""',
                icon=str(icons_folder_path / 'check.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


# hash create
@hash_cmd.command(
    help=f"""
        {_('Creates hash file (.sha256, .sha1, etc).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor hash create file1.jpg file2.pdf file3.exe -f sha256` 

- `file_conversor hash create file1.jpg file2.pdf -f sha1 -od D:/Downloads` 
""")
def create(
    input_files: InputFilesArgument(),  # pyright: ignore[reportInvalidTypeForm]
    format: FormatOption(HashBackend),  # pyright: ignore[reportInvalidTypeForm]
    output_dir: OutputDirOption() = Path(),  # pyright: ignore[reportInvalidTypeForm]
):
    output_file = output_dir / f"CHECKSUM.{format}"
    if not STATE["overwrite"]:
        check_path_exists(output_file, exists=False)

    hash_backend = HashBackend(
        verbose=STATE["verbose"],
    )
    with ProgressManager() as progress_mgr:
        hash_backend.generate(
            input_files=input_files,
            output_file=output_file,
            progress_callback=progress_mgr.update_progress,
        )
        progress_mgr.complete_step()

    logger.info(f"{_('Hash creation')}: [bold green]{_('SUCCESS')}[/].")


# hash check
@hash_cmd.command(
    help=f"""
        {_('Checks a hash file (.sha256, .sha1, etc).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor hash check file.sha256` 
- `file_conversor hash check file.sha1 file.sha3_512` 
""")
def check(
    input_files: InputFilesArgument(HashBackend),  # pyright: ignore[reportInvalidTypeForm]
):
    exception = None
    hash_backend = HashBackend(verbose=STATE["verbose"])

    with ProgressManager(len(input_files)) as progress_mgr:
        for input_file in input_files:
            try:
                logger.info(f"{_('Checking file')} '{input_file}' ...")
                hash_backend.check(
                    input_file=input_file,
                    progress_callback=progress_mgr.update_progress,
                )
            except Exception as e:
                logger.error(repr(e))
                exception = e
            progress_mgr.complete_step()

    if exception:
        logger.info(f"{_('Hash check')}: [bold red]{_('FAILED')}[/].")
        raise typer.Exit(1)
    logger.info(f"{_('Hash check')}: [bold green]{_('SUCCESS')}[/].")
