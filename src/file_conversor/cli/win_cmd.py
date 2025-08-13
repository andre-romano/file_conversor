
# src\file_conversor\cli\win_cmd.py

import typer

from typing import Annotated

from rich import print


# user-provided modules
from file_conversor.backend import WinRegBackend

from file_conversor.config import Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.system import win
from file_conversor.system.win.ctx_menu import WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

win_cmd = typer.Typer()

# PANELS
CONTEXT_MENU_PANEL = _("Context menu")


# win restart-explorer
@win_cmd.command(
    help=f"""
        {_('Restarts explorer.exe (to refresh ctx menus).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor win restart-explorer` 
""")
def restart_explorer():
    logger.info(f"{_('Restarting explorer.exe')} ...")
    win.restart_explorer()


# win install-menu
@win_cmd.command(
    rich_help_panel=CONTEXT_MENU_PANEL,
    help=f"""
        {_('Installs app context menu (right click in Windows Explorer).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor win install-menu` 
""")
def install_menu(
    reboot_explorer: Annotated[bool, typer.Option("--restart-explorer", "-re",
                                                  help=_("Restart explorer.exe (to make ctx menu effective immediately). Defaults to False (do not restart, user must log off/in to make ctx menu changes effective)"),
                                                  is_flag=True,
                                                  )] = False,
):
    winreg_backend = WinRegBackend(verbose=STATE["verbose"])

    logger.info(f"{_('Installing app context menu in Windows Explorer')} ...")

    # Define registry path
    ctx_menu = WinContextMenu.get_instance()
    # logger.debug("---- .REG file contents ----")
    # logger.debug(repr(ctx_menu.get_reg_file()))

    winreg_backend.import_file(ctx_menu.get_reg_file())

    if reboot_explorer:
        restart_explorer()
    else:
        logger.warning("Restart explorer.exe or log off from Windows, to make changes effective immediately.")

    logger.info(f"{_('Context Menu Install')}: [bold green]{_('SUCCESS')}[/].")


# win uninstall-menu
@win_cmd.command(
    rich_help_panel=CONTEXT_MENU_PANEL,
    help=f"""
        {_('Uninstalls app context menu (right click in Windows Explorer).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor win uninstall-menu` 
""")
def uninstall_menu():
    winreg_backend = WinRegBackend(verbose=STATE["verbose"])

    logger.info(f"{_('Removing app context menu from Windows Explorer')} ...")

    # Define registry path
    ctx_menu = WinContextMenu.get_instance()
    # logger.debug("---- .REG file contents ----")
    # logger.debug(repr(ctx_menu.get_reg_file()))

    winreg_backend.delete_keys(ctx_menu.get_reg_file())

    logger.info(f"{_('Context Menu Uninstall')}: [bold green]{_('SUCCESS')}[/].")
