
# src\file_conversor\cli\config\__init__.py


import typer

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli.config._typer import COMMAND_NAME

from file_conversor.cli.config.set_cmd import typer_cmd as set_cmd
from file_conversor.cli.config.show_cmd import typer_cmd as show_cmd

_ = get_translation()

config_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=_("Configure default options"),
)
config_cmd.add_typer(show_cmd)
config_cmd.add_typer(set_cmd)

__all__ = [
    "config_cmd",
]
