# src\file_conversor\cli\gui\__init__.py

import typer

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli.gui._typer import COMMAND_NAME

from file_conversor.cli.gui.start_cmd import typer_cmd as start_cmd

_ = get_translation()

gui_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=_("Graphical User Interface commands"),
)

gui_cmd.add_typer(start_cmd)

__all__ = [
    "gui_cmd",
]
