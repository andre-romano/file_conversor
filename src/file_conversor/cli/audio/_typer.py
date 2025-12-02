# src\file_conversor\cli\audio\_typer.py

# user-provided modules
from file_conversor.config import get_translation

_ = get_translation()

# command
COMMAND_NAME = "audio"

# SUBCOMMANDS
CHECK_NAME = "check"
CONVERT_NAME = "convert"
INFO_NAME = "info"

__all__ = [
    "COMMAND_NAME",

    "CHECK_NAME",
    "CONVERT_NAME",
    "INFO_NAME",
]
