
# src\file_conversor\cli\svg_cmd.py

import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend import PyMuSVGBackend

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.rich import get_progress_bar
from file_conversor.utils.validators import check_file_format

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

svg_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # PyMuSVGBackend commands
    for ext in PyMuSVGBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_jpg",
                description="To JPG",
                command=f'{Environment.get_executable()} svg convert "%1" -o "%1.jpg"',
                icon=str(icons_folder_path / 'jpg.ico'),
            ),
            WinContextCommand(
                name="to_png",
                description="To PNG",
                command=f'{Environment.get_executable()} svg convert "%1" -o "%1.png"',
                icon=str(icons_folder_path / 'png.ico'),
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

        - `file_conversor svg convert input_file.svg -o output_file.jpg --dpi 300`

        - `file_conversor svg convert input_file.svg -o output_file.png`
    """)
def convert(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file')} ({', '.join(PyMuSVGBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PyMuSVGBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    output_file: Annotated[str, typer.Option("--output", "-o",
                                             help=f"{_('Output file')} ({', '.join(PyMuSVGBackend.SUPPORTED_OUT_FORMATS)})",
                                             callback=lambda x: check_file_format(x, PyMuSVGBackend.SUPPORTED_OUT_FORMATS),
                                             )],

    dpi: Annotated[int, typer.Option("--dpi", "-d",
                                     help=_("Image quality in dots per inch (DPI). Valid values are between 40-3600."),
                                     min=40, max=3600,
                                     )] = CONFIG["image-dpi"],
):
    pymusvg_backend = PyMuSVGBackend(verbose=STATE['verbose'])
    # display current progress
    with get_progress_bar() as progress:
        task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None)
        pymusvg_backend.convert(
            input_file=input_file,
            output_file=output_file,
            dpi=dpi,
        )
        progress.update(task, total=100, completed=100)
    logger.info(f"{_('File convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
