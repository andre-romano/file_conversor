# src\file_conversor\cli\ppt\__init__.py

import typer

# user-provided modules
from file_conversor.cli.ppt.convert_cmd import typer_cmd as convert_cmd

ppt_cmd = typer.Typer()
ppt_cmd.add_typer(convert_cmd)
