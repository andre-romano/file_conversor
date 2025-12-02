# src\file_conversor\cli\doc\__init__.py

import typer

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli.doc._typer import COMMAND_NAME

from file_conversor.cli.doc.convert_cmd import typer_cmd as convert_cmd

_ = get_translation()


doc_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=f"{_('Document file manipulation')} {_('(requires LibreOffice)')})",
)
doc_cmd.add_typer(convert_cmd)

__all__ = [
    "doc_cmd",
]
