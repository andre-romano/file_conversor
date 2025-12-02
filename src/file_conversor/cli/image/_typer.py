# src\file_conversor\cli\image\_typer.py

# user-provided modules
from file_conversor.config import get_translation

_ = get_translation()

CONVERSION_PANEL = _("Conversions")
TRANSFORMATION_PANEL = _("Transformations")
FILTER_PANEL = _("Filters")
OTHERS_PANEL = _("Other commands")

# command
COMMAND_NAME = "image"

# SUBCOMMANDS
ANTIALIAS_NAME = "antialias"
BLUR_NAME = "blur"
COMPRESS_NAME = "compress"
CONVERT_NAME = "convert"
ENHANCE_NAME = "enhance"
FILTER_NAME = "filter"
INFO_NAME = "info"
MIRROR_NAME = "mirror"
RENDER_NAME = "render"
RESIZE_NAME = "resize"
ROTATE_NAME = "rotate"
TO_PDF_NAME = "to-pdf"
UNSHARP_NAME = "unsharp"

__all__ = [
    "COMMAND_NAME",

    "ANTIALIAS_NAME",
    "BLUR_NAME",
    "COMPRESS_NAME",
    "CONVERT_NAME",
    "ENHANCE_NAME",
    "FILTER_NAME",
    "INFO_NAME",
    "MIRROR_NAME",
    "RENDER_NAME",
    "RESIZE_NAME",
    "ROTATE_NAME",
    "TO_PDF_NAME",
    "UNSHARP_NAME",
]
