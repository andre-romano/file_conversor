# src\file_conversor\cli\hash\__init__.py

import typer

# user-provided modules
from file_conversor.cli.hash.check_cmd import typer_cmd as check_cmd
from file_conversor.cli.hash.create_cmd import typer_cmd as create_cmd

hash_cmd = typer.Typer()
hash_cmd.add_typer(create_cmd)
hash_cmd.add_typer(check_cmd)
