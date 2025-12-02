# src\file_conversor\cli\pipeline\_info.py

# user-provided modules
from file_conversor.config import get_translation

_ = get_translation()

# command
COMMAND_NAME = "pipeline"

# SUBCOMMANDS
CREATE_NAME = "create"
EXECUTE_NAME = "execute"

__all__ = [
    "COMMAND_NAME",

    "CREATE_NAME",
    "EXECUTE_NAME",
]
