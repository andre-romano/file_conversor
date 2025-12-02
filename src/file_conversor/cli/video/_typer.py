# src\file_conversor\cli\vidio\_typer.py

# user-provided modules
from file_conversor.config import get_translation

_ = get_translation()

TRANSFORMATION_PANEL = _("Transformations")
OTHERS_PANEL = _("Other commands")

# command
COMMAND_NAME = "video"

# SUBCOMMANDS
CHECK_NAME = "check"
COMPRESS_NAME = "compress"
CONVERT_NAME = "convert"
ENHANCE_NAME = "enhance"
EXECUTE_NAME = "execute"
INFO_NAME = "info"
LIST_FORMATS_NAME = "list-formats"
MIRROR_NAME = "mirror"
RESIZE_NAME = "resize"
ROTATE_NAME = "rotate"

__all__ = [
    "COMMAND_NAME",

    "CHECK_NAME",
    "COMPRESS_NAME",
    "CONVERT_NAME",
    "ENHANCE_NAME",
    "EXECUTE_NAME",
    "INFO_NAME",
    "LIST_FORMATS_NAME",
    "MIRROR_NAME",
    "RESIZE_NAME",
    "ROTATE_NAME",
]
