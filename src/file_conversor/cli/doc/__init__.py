# src\file_conversor\cli\doc\__init__.py

import typer

# user-provided modules
from file_conversor.cli.doc.convert_cmd import typer_cmd as convert_cmd


doc_cmd = typer.Typer()
doc_cmd.add_typer(convert_cmd)
