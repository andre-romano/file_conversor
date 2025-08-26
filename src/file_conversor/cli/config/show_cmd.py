
# src\file_conversor\cli\config\show_cmd.py

import typer

from typing import Annotated

from rich import print
from rich.pretty import Pretty

# user-provided modules
from file_conversor.config import Configuration, State, Log, get_translation

# app configuration
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# create command
typer_cmd = typer.Typer()


# config show
@typer_cmd.command(help=f"""
    {_('Show the current configuration of the application')}.
""")
def show():
    print(f"{_('Configuration')}:", Pretty(CONFIG.to_dict(), expand_all=True))
