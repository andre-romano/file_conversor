
# src\file_conversor\cli\xls_cmd.py

import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend import XLS_BACKEND

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.progress_manager import ProgressManager
from file_conversor.utils.validators import *

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# typer PANELS
xls_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # WordBackend commands
    for ext in XLS_BACKEND.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name=f"to_{ext}",
                description=f"To {ext.upper()}",
                command=f'{Environment.get_executable()} xls convert "%1" -o "%1.{ext}"',
                icon=str(icons_folder_path / f"{ext}.ico"),
            ) for ext in XLS_BACKEND.SUPPORTED_OUT_FORMATS
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


# xls convert
@xls_cmd.command(
    help=f"""
        {_('Convert spreadsheet files into other formats (requires Microsoft Word / LibreOffice).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor doc convert input_file.ods -o output_file.xls`

        - `file_conversor doc convert input_file.xlsx -o output_file.pdf`
    """)
def convert(
    input_files: Annotated[List[Path], typer.Argument(help=f"{_('Input files')} ({', '.join(XLS_BACKEND.SUPPORTED_IN_FORMATS)})",
                                                      callback=lambda x: check_file_format(x, XLS_BACKEND.SUPPORTED_IN_FORMATS, exists=True),
                                                      )],

    format: Annotated[str, typer.Option("--format", "-f",
                                        help=f"{_('Output format')} ({', '.join(XLS_BACKEND.SUPPORTED_OUT_FORMATS)})",
                                        callback=lambda x: check_valid_options(x, XLS_BACKEND.SUPPORTED_OUT_FORMATS),
                                        )],

    output_dir: Annotated[Path, typer.Option("--output-dir", "-od",
                                             help=f"{_('Output directory')}. {_('Defaults to current working directory')}.",
                                             callback=lambda x: check_dir_exists(x, mkdir=True),
                                             )] = Path(),
):
    xls_backend = XLS_BACKEND(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )

    with ProgressManager(len(input_files)) as progress_mgr:
        for input_file in input_files:
            output_file = output_dir / Environment.get_output_file(input_file, suffix=f".{format}")
            if not STATE["overwrite"]:
                check_path_exists(output_file, exists=False)

            xls_backend.convert(
                input_file=input_file,
                output_file=output_file,
            )
            progress_mgr.complete_step()

    logger.info(f"{_('File conversion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
