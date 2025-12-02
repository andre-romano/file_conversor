# src\file_conversor\cli\pdf\__init__.py

import typer

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli.pdf._typer import COMMAND_NAME

from file_conversor.cli.pdf.compress_cmd import typer_cmd as compress_cmd
from file_conversor.cli.pdf.convert_cmd import typer_cmd as convert_cmd
from file_conversor.cli.pdf.decrypt_cmd import typer_cmd as decrypt_cmd
from file_conversor.cli.pdf.encrypt_cmd import typer_cmd as encrypt_cmd
from file_conversor.cli.pdf.extract_cmd import typer_cmd as extract_cmd
from file_conversor.cli.pdf.extract_img_cmd import typer_cmd as extract_img_cmd
from file_conversor.cli.pdf.merge_cmd import typer_cmd as merge_cmd
from file_conversor.cli.pdf.ocr_cmd import typer_cmd as ocr_cmd
from file_conversor.cli.pdf.repair_cmd import typer_cmd as repair_cmd
from file_conversor.cli.pdf.rotate_cmd import typer_cmd as rotate_cmd
from file_conversor.cli.pdf.split_cmd import typer_cmd as split_cmd

_ = get_translation()

pdf_cmd = typer.Typer(
    name=COMMAND_NAME,
    help=_("PDF file manipulation"),
)
# SECURITY_PANEL
pdf_cmd.add_typer(encrypt_cmd)
pdf_cmd.add_typer(decrypt_cmd)

# TRANSFORMATION_PANEL
pdf_cmd.add_typer(compress_cmd)
pdf_cmd.add_typer(extract_cmd)
pdf_cmd.add_typer(merge_cmd)
pdf_cmd.add_typer(rotate_cmd)
pdf_cmd.add_typer(split_cmd)
pdf_cmd.add_typer(ocr_cmd)

# OTHERS_PANEL
pdf_cmd.add_typer(convert_cmd)
pdf_cmd.add_typer(extract_img_cmd)
pdf_cmd.add_typer(repair_cmd)

__all__ = [
    "pdf_cmd",
]
