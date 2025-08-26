
# src\file_conversor\cli\config\__init__.py


import typer

# user-provided modules
from file_conversor.cli.config.set_cmd import typer_cmd as set_cmd
from file_conversor.cli.config.show_cmd import typer_cmd as show_cmd

config_cmd = typer.Typer()
config_cmd.add_typer(show_cmd)
config_cmd.add_typer(set_cmd)
