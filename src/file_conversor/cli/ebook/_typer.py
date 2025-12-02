# src\file_conversor\cli\ebook\_typer.py

# user-provided modules
from file_conversor.config import get_translation

_ = get_translation()

# command
COMMAND_NAME = "ebook"

# SUBCOMMANDS
CONVERT_NAME = "convert"

__all__ = [
    "COMMAND_NAME",

    "CONVERT_NAME",
]
