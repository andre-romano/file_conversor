
# src\file_conversor\cli\win\restart_exp_cmd.py

import typer

from typing import Annotated

from rich import print


# user-provided modules
from file_conversor.cli.win._typer import OTHERS_PANEL as RICH_HELP_PANEL
from file_conversor.cli.win._typer import COMMAND_NAME, RESTART_EXPLORER_NAME

from file_conversor.config import Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.system import win

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = set()


@typer_cmd.command(
    name=RESTART_EXPLORER_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Restarts explorer.exe (to refresh ctx menus).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor {COMMAND_NAME} {RESTART_EXPLORER_NAME}` 
""")
def restart_explorer():
    logger.info(f"{_('Restarting explorer.exe')} ...")
    win.restart_explorer()


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
