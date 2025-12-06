
# src\file_conversor\cli\win\unins_cmd.py

import typer

from typing import Annotated

from rich import print


# user-provided modules
from file_conversor.backend import WinRegBackend

from file_conversor.cli.win._typer import CONTEXT_MENU_PANEL as RICH_HELP_PANEL
from file_conversor.cli.win._typer import COMMAND_NAME, UNINSTALL_MENU_NAME

from file_conversor.config import Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.system.win.ctx_menu import WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = WinRegBackend.EXTERNAL_DEPENDENCIES


@typer_cmd.command(
    name=UNINSTALL_MENU_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Uninstalls app context menu (right click in Windows Explorer).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor {COMMAND_NAME} {UNINSTALL_MENU_NAME}` 
""")
def uninstall_menu():
    winreg_backend = WinRegBackend(verbose=STATE["verbose"])

    logger.info(f"{_('Removing app context menu from Windows Explorer')} ...")

    # Define registry path
    ctx_menu = WinContextMenu.get_instance()

    winreg_backend.delete_keys(ctx_menu.get_reg_file())

    logger.info(f"{_('Context Menu Uninstall')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
