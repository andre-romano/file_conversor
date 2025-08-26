# src\file_conversor\cli\text\__init__.py

import typer

# user-provided modules
from file_conversor.cli.text.check_cmd import typer_cmd as check_cmd
from file_conversor.cli.text.compress_cmd import typer_cmd as compress_cmd
from file_conversor.cli.text.convert_cmd import typer_cmd as convert_cmd

text_cmd = typer.Typer()
text_cmd.add_typer(check_cmd)
text_cmd.add_typer(compress_cmd)
text_cmd.add_typer(convert_cmd)
