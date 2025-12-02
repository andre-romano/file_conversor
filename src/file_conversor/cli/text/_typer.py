# src\file_conversor\cli\text\_typer.py

# user-provided modules
from file_conversor.config import get_translation

_ = get_translation()

# command
COMMAND_NAME = "text"

# SUBCOMMANDS
CHECK_NAME = "check"
COMPRESS_NAME = "compress"
CONVERT_NAME = "convert"

__all__ = [
    "COMMAND_NAME",

    "CHECK_NAME",
    "COMPRESS_NAME",
    "CONVERT_NAME",
]
