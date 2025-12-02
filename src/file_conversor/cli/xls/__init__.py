# src\file_conversor\cli\xls\__init__.py

import typer

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli.xls._typer import COMMAND_NAME

from file_conversor.cli.xls.convert_cmd import typer_cmd as convert_cmd

_ = get_translation()

xls_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=f"{_('Spreadsheet file manipulation')} {_('(requires LibreOffice)')})",
)
xls_cmd.add_typer(convert_cmd)

__all__ = [
    "xls_cmd",
]
