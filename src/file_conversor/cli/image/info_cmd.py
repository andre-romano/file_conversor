
# src\file_conversor\cli\image\info_cmd.py

import typer

from pathlib import Path
from typing import Annotated, List

from rich import print
from rich.panel import Panel
from rich.console import Group

# user-provided modules
from file_conversor.backend.image import PillowBackend

from file_conversor.cli.image._typer import OTHERS_PANEL as RICH_HELP_PANEL
from file_conversor.cli.image._typer import COMMAND_NAME, INFO_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.backend import PillowParser
from file_conversor.utils.typer_utils import InputFilesArgument

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # Pillow commands
    for ext in PillowBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="info",
                description="Get Info",
                command=f'cmd.exe /k "{Environment.get_executable()} "{COMMAND_NAME}" "{INFO_NAME}" "%1""',
                icon=str(icons_folder_path / "info.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=INFO_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Get EXIF information about a image file.')}

        {_('This command retrieves metadata and other information about the image file')}:
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {COMMAND_NAME} {INFO_NAME} other_filename.jpg`

        - `file_conversor {COMMAND_NAME} {INFO_NAME} filename.webp filename2.png filename3.gif`
    """)
def info(
    input_files: Annotated[List[str], InputFilesArgument(PillowBackend)],
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])
    for input_file in input_files:

        # 📁 Informações gerais do arquivo
        parser = PillowParser(pillow_backend, Path(input_file))
        parser.run()

        # Agrupar e exibir tudo com Rich
        group = Group(
            *parser.get_exif_info().rich(),
        )
        print(Panel(group, title=f"🧾 {_('File Analysis')}", border_style="blue"))


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
