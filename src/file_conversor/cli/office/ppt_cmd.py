
# src\file_conversor\cli\ppt_cmd.py

import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend import PPT_BACKEND

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.rich import get_progress_bar
from file_conversor.utils.validators import check_file_format

from file_conversor.system import CURR_PLATFORM, PLATFORM_WINDOWS
from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# typer PANELS
ppt_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # WordBackend commands
    for ext in PPT_BACKEND.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name=f"to_{ext}",
                description=f"To {ext.upper()}",
                command=f'{Environment.get_executable()} ppt convert "%1" -o "%1.{ext}"',
                icon=str(icons_folder_path / f"{ext}.ico"),
            ) for ext in PPT_BACKEND.SUPPORTED_OUT_FORMATS
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


# xls convert
@ppt_cmd.command(
    help=f"""
        {_('Convert presentation files into other formats (requires Microsoft Word / LibreOffice).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor ppt convert input_file.odp -o output_file.ppt`

        - `file_conversor ppt convert input_file.pptx -o output_file.pdf`
    """)
def convert(
    input_file: Annotated[str, typer.Argument(help=f"{_('Input file')} ({', '.join(PPT_BACKEND.SUPPORTED_IN_FORMATS)})",
                                              callback=lambda x: check_file_format(x, PPT_BACKEND.SUPPORTED_IN_FORMATS, exists=True),
                                              )],

    output_file: Annotated[str, typer.Option("--output", "-o",
                                             help=f"{_('Output file')} ({', '.join(PPT_BACKEND.SUPPORTED_OUT_FORMATS)}). {_('Defaults to None')} ({_('use the same input file as output name')}).",
                                             callback=lambda x: check_file_format(x, PPT_BACKEND.SUPPORTED_OUT_FORMATS),
                                             )],
):
    ppt_backend = PPT_BACKEND(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )

    logger.info(f"{_('Processing file')} '{input_file}' => '{output_file}' ...")

    with get_progress_bar() as progress:
        task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None)
        ppt_backend.convert(
            input_file=input_file,
            output_file=output_file,
        )
        progress.update(task, total=100, completed=100)

    logger.info(f"{_('File conversion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
