
# src\file_conversor\cli\utils\hash_cmd.py

import typer

from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend import HashBackend

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

from file_conversor.utils.rich import get_progress_bar
from file_conversor.utils.validators import check_file_format, check_valid_options

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
                command=f'{Environment.get_executable()} hash check "%1"',
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

- `file_conversor hash create file1.jpg file2.pdf file3.exe -o file.sha256` 
""")
def create(
    input_files: Annotated[List[str], typer.Argument(
        help=f"{_('Input files')}",
    )],

    output_file: Annotated[str, typer.Option("--output", "-o",
                                             help=f"{_('Output file')} ({', '.join(HashBackend.SUPPORTED_OUT_FORMATS)}).",
                                             callback=lambda x: check_file_format(x, HashBackend.SUPPORTED_OUT_FORMATS)
                                             )],
):
    hash_backend = HashBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        input_len = len(input_files)
        task = progress.add_task(f"{_('Processing files')}:", total=input_len,)
        hash_backend.generate(
            input_files=input_files,
            output_file=output_file,
            progress_callback=lambda p: progress.update(task, completed=p),
        )

    logger.info(f"{_('Hash creation')}: [bold green]{_('SUCCESS')}[/].")


# hash check
@hash_cmd.command(
    help=f"""
        {_('Checks a hash file (.sha256, .sha1, etc).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor hash check file.sha256` 
""")
def check(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file')} ({', '.join(HashBackend.SUPPORTED_IN_FORMATS)})",
    )],
):
    hash_backend = HashBackend(verbose=STATE["verbose"])
    logger.info(f"{_('Checking file hashes ...')}")

    hash_backend.check(
        input_file=input_file,
    )

    logger.info(f"{_('Hash check')}: [bold green]{_('SUCCESS')}[/].")
