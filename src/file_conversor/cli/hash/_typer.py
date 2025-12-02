# src\file_conversor\cli\hash\_typer.py

# user-provided modules
from file_conversor.config import get_translation

_ = get_translation()

COMMAND_NAME = "hash"

# SUBCOMMANDS
CHECK_NAME = "check"
CREATE_NAME = "create"

__all__ = [
    "COMMAND_NAME",

    "CHECK_NAME",
    "CREATE_NAME",
]
