
# src\file_conversor\cli\config\show_cmd.py

import typer

from typing import Annotated

from rich import print
from rich.pretty import Pretty

# user-provided modules
from file_conversor.cli.config._typer import COMMAND_NAME, SHOW_NAME
from file_conversor.config import Configuration, State, Log, get_translation

# app configuration
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# create command
typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = set()


# config show
@typer_cmd.command(
    name=SHOW_NAME,
    help=f"""
        {_('Show the current configuration of the application')}.
    """,
    epilog=f"""
    **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {SHOW_NAME}`
    """
)
def show():
    print(f"{_('Configuration')}:", Pretty(CONFIG.to_dict(), expand_all=True))


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
