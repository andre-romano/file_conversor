# src\file_conversor\cli\pipeline\__init__.py

import typer

# user-provided modules
from file_conversor.config import get_translation

from file_conversor.cli.pipeline.create_cmd import typer_cmd as create_cmd
from file_conversor.cli.pipeline.execute_cmd import typer_cmd as execute_cmd

_ = get_translation()


pipeline_cmd = typer.Typer()
pipeline_cmd.add_typer(create_cmd)
pipeline_cmd.add_typer(execute_cmd)
