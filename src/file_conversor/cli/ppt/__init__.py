# src\file_conversor\cli\ppt\__init__.py

import typer

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli.ppt._typer import COMMAND_NAME

from file_conversor.cli.ppt.convert_cmd import typer_cmd as convert_cmd

_ = get_translation()

ppt_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=f"{_('Presentation file manipulation')} {_('(requires LibreOffice)')})",
)
ppt_cmd.add_typer(convert_cmd)

__all__ = [
    "ppt_cmd",
]
