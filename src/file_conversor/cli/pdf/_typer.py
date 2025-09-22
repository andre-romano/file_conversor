# src\file_conversor\cli\pdf\_info.py

# user-provided modules
from file_conversor.config import get_translation

_ = get_translation()

SECURITY_PANEL = _(f"Security commands")
TRANSFORMATION_PANEL = _("Transformations")
OTHERS_PANEL = _("Other commands")

# command
COMMAND_NAME = "pdf"

# SUBCOMMANDS
COMPRESS_NAME = "compress"
CONVERT_NAME = "convert"

DECRYPT_NAME = "decrypt"
ENCRYPT_NAME = "encrypt"

EXTRACT_NAME = "extract"
EXTRACT_IMG_NAME = "extract-img"

MERGE_NAME = "merge"
OCR_NAME = "ocr"
REPAIR_NAME = "repair"

ROTATE_NAME = "rotate"
SPLIT_NAME = "split"
