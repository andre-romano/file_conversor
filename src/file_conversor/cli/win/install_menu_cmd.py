
# src\file_conversor\cli\win\inst_menu_cmd.py

import typer

from typing import Annotated

from rich import print


# user-provided modules
from file_conversor.backend import WinRegBackend

import file_conversor.cli.win.uninstall_menu_cmd as uninstall_menu_cmd
import file_conversor.cli.win.restart_explorer_cmd as restart_explorer_cmd

from file_conversor.cli.win._typer import CONTEXT_MENU_PANEL as RICH_HELP_PANEL
from file_conversor.cli.win._typer import COMMAND_NAME, INSTALL_MENU_NAME

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
    name=INSTALL_MENU_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Installs app context menu (right click in Windows Explorer).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor {COMMAND_NAME} {INSTALL_MENU_NAME}` 
""")
def install_menu(
    reboot_explorer: Annotated[bool, typer.Option("--restart-explorer", "-re",
                                                  help=_("Restart explorer.exe (to make ctx menu effective immediately). Defaults to False (do not restart, user must log off/in to make ctx menu changes effective)"),
                                                  is_flag=True,
                                                  )] = False,
):
    winreg_backend = WinRegBackend(verbose=STATE["verbose"])

    uninstall_menu_cmd.uninstall_menu()

    logger.info(f"{_('Installing app context menu in Windows Explorer')} ...")

    # Define registry path
    ctx_menu = WinContextMenu.get_instance()

    winreg_backend.import_file(ctx_menu.get_reg_file())

    if reboot_explorer:
        restart_explorer_cmd.restart_explorer()
    else:
        logger.warning("Restart explorer.exe or log off from Windows, to make changes effective immediately.")

    logger.info(f"{_('Context Menu Install')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
