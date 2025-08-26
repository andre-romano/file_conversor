# src\file_conversor\cli\xls\__init__.py

import typer

# user-provided modules
from file_conversor.cli.xls.convert_cmd import typer_cmd as convert_cmd

xls_cmd = typer.Typer()
xls_cmd.add_typer(convert_cmd)
