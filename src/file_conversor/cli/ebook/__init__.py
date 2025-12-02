
# src\file_conversor\cli\ebook\__init__.py


import typer

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli.ebook._typer import COMMAND_NAME

from file_conversor.cli.ebook.convert_cmd import typer_cmd as convert_cmd

_ = get_translation()

ebook_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=_("Ebook file manipulation (requires Calibre external library)"),
)

# CONVERSION_PANEL
ebook_cmd.add_typer(convert_cmd)

__all__ = [
    "ebook_cmd",
]
