
# src\file_conversor\cli\doc_cmd.py

import re
import time
import typer

from pathlib import Path
from typing import Annotated, List, Optional

from rich import print

# user-provided modules
from file_conversor.backend import WordBackend, WriterBackend

from file_conversor.config import Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.rich import get_progress_bar
from file_conversor.utils.validators import check_file_format, check_valid_options

from file_conversor.system import CURR_PLATFORM, PLATFORM_WINDOWS
from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# typer PANELS
doc_cmd = typer.Typer()

OfficeBackend = WordBackend if CURR_PLATFORM == PLATFORM_WINDOWS else WriterBackend


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = State.get_icons_folder()
    # WordBackend commands
    for ext in OfficeBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name=f"to_{ext}",
                description=f"To {ext.upper()}",
                command=f'{State.get_executable()} doc convert "%1" "%1.{ext}"',
                icon=str(icons_folder_path / f"{ext}.ico"),
            ) for ext in OfficeBackend.SUPPORTED_OUT_FORMATS
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


# doc to-pdf
@doc_cmd.command(
    help=f"""
        {_('Convert document files into other formats (requires Microsoft Word / LibreOffice).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor doc convert input_file.odt -o output_file.doc`

        - `file_conversor doc convert input_file.docx -o output_file.pdf`
    """)
def convert(
    input_file: Annotated[str, typer.Argument(help=f"{_('Input file')} ({', '.join(WordBackend.SUPPORTED_IN_FORMATS)})",
                                              callback=lambda x: check_file_format(x, WordBackend.SUPPORTED_IN_FORMATS, exists=True),
                                              )],

    output_file: Annotated[str, typer.Option("--output", "-o",
                                             help=f"{_('Output file')} ({', '.join(WordBackend.SUPPORTED_OUT_FORMATS)}). {_('Defaults to None')} ({_('use the same input file as output name')}).",
                                             callback=lambda x: check_file_format(x, WordBackend.SUPPORTED_OUT_FORMATS),
                                             )],
):
    office_backend = OfficeBackend()

    logger.info(f"{_('Processing file')} '{input_file}' => '{output_file}' ...")

    with get_progress_bar() as progress:
        task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None)
        office_backend.convert(
            input_file=input_file,
            output_file=output_file,
        )
        progress.update(task, total=100, completed=100)

    logger.info(f"{_('File conversion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
