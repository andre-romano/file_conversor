
# src\file_conversor\cli\gui\start_cmd.py

import typer

from typing import Annotated

from rich import print


# user-provided modules
from file_conversor.backend.gui import WebApp

from file_conversor.cli.gui._typer import COMMAND_NAME, START_NAME

from file_conversor.config import Configuration, State, Log
from file_conversor.config.locale import get_translation

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES: set[str] = set()


@typer_cmd.command(
    name=START_NAME,
    help=f"""
        {_('Starts the graphical user interface.')}
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor {COMMAND_NAME} {START_NAME}`
    """
)
def start_gui():
    logger.info(f"[bold]{_('Starting the graphical user interface')} ...[/]")
    webapp = WebApp.get_instance()
    webapp.run()


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
