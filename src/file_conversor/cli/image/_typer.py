# src\file_conversor\cli\image\_typer.py

# user-provided modules
from file_conversor.config import get_translation

_ = get_translation()

CONVERSION_PANEL = _("Conversion")
TRANSFORMATION_PANEL = _("Transformation")
OTHERS_PANEL = _("Other commands")

# command
COMMAND_NAME = "image"

# SUBCOMMANDS
COMPRESS_NAME = "compress"
CONVERT_NAME = "convert"
INFO_NAME = "info"
MIRROR_NAME = "mirror"
RENDER_NAME = "render"
RESIZE_NAME = "resize"
ROTATE_NAME = "rotate"
TO_PDF_NAME = "to-pdf"
