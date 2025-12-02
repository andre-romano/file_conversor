# src\file_conversor\cli\hash\__init__.py

import typer

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli.hash._typer import COMMAND_NAME

from file_conversor.cli.hash.check_cmd import typer_cmd as check_cmd
from file_conversor.cli.hash.create_cmd import typer_cmd as create_cmd

_ = get_translation()

hash_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=_("Hashing manipulation (check, gen, etc)"),
)
hash_cmd.add_typer(create_cmd)
hash_cmd.add_typer(check_cmd)

__all__ = [
    "hash_cmd",
]
