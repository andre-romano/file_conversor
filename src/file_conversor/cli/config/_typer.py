# src\file_conversor\cli\config\_typer.py

# user-provided modules
from file_conversor.config import get_translation

_ = get_translation()

COMMAND_NAME = "config"

# SUBCOMMANDS
SET_NAME = "set"
SHOW_NAME = "show"

__all__ = [
    "COMMAND_NAME",

    "SET_NAME",
    "SHOW_NAME",
]
