
# src\file_conversor\cli\svg_cmd.py

import typer

from pathlib import Path
from typing import Annotated, List

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.console import Group

# user-provided modules
from file_conversor.backend import PyMuPDFBackend

from file_conversor.config import Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import File
from file_conversor.utils.rich import get_progress_bar
from file_conversor.utils.validators import check_file_format, check_is_bool_or_none, check_valid_options

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

svg_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = State.get_icons_folder()
    # PyMuPDFBackend commands
    for ext in PyMuPDFBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_png",
                description="To PNG",
                command=f'{State.get_executable()} svg convert "%1" -o "%1.png"',
                icon=str(icons_folder_path / 'png.ico'),
            ),
            WinContextCommand(
                name="to_pdf",
                description="To PDF",
                command=f'{State.get_executable()} svg convert "%1" -o "%1.pdf"',
                icon=str(icons_folder_path / 'pdf.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


# image convert
@svg_cmd.command(
    help=f"""
        {_('Convert a SVG file to a different format.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor svg convert input_file.svg -o output_file.pdf --dpi 300`

        - `file_conversor svg convert input_file.svg -o output_file.png`
    """)
def convert(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file')} ({', '.join(PyMuPDFBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PyMuPDFBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    output_file: Annotated[str, typer.Option("--output", "-o",
                                             help=f"{_('Output file')} ({', '.join(PyMuPDFBackend.SUPPORTED_OUT_FORMATS)})",
                                             callback=lambda x: check_file_format(x, PyMuPDFBackend.SUPPORTED_OUT_FORMATS),
                                             )],

    dpi: Annotated[int, typer.Option("--dpi", "-d",
                                     help=_("Image quality in dots per inch (DPI). Valid values are between 40-3600."),
                                     min=40, max=3600,
                                     )] = CONFIG["image-dpi"],
):
    pymupdf_backend = PyMuPDFBackend(verbose=STATE['verbose'])
    # display current progress
    with get_progress_bar() as progress:
        task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None)
        pymupdf_backend.convert(
            input_file=input_file,
            output_file=output_file,
            dpi=dpi,
        )
        progress.update(task, total=100, completed=100)
    logger.info(f"{_('SVG convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
