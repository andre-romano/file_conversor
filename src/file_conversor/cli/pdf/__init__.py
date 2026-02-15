# src\file_conversor\cli\pdf\__init__.py

from enum import Enum

from file_conversor.cli._utils.abstract_typer_group import AbstractTyperGroup
from file_conversor.cli.pdf.compress_cli import PdfCompressCLI
from file_conversor.cli.pdf.convert_cli import PdfConvertCLI
from file_conversor.cli.pdf.decrypt_cli import PdfDecryptCLI
from file_conversor.cli.pdf.encrypt_cli import PdfEncryptCLI
from file_conversor.cli.pdf.extract_cli import PdfExtractCLI
from file_conversor.cli.pdf.extract_img_cli import PdfExtractImgCLI
from file_conversor.cli.pdf.merge_cli import PdfMergeCLI
from file_conversor.cli.pdf.ocr_cli import PdfOcrCLI
from file_conversor.cli.pdf.repair_cli import PdfRepairCLI
from file_conversor.cli.pdf.rotate_cli import PdfRotateCLI
from file_conversor.cli.pdf.split_cli import PdfSplitCLI
from file_conversor.config.locale import get_translation


_ = get_translation()


class PdfTyperGroup(AbstractTyperGroup):

    class Panels(Enum):
        SECURITY = _(f"Security commands")
        TRANSFORMATION = _("Transformations")
        OTHERS = _("Other commands")

    class Commands(Enum):
        # SECURITY_PANEL
        DECRYPT = "decrypt"
        ENCRYPT = "encrypt"

        # TRANSFORMATION_PANEL
        COMPRESS = "compress"
        EXTRACT = "extract"
        MERGE = "merge"
        ROTATE = "rotate"
        SPLIT = "split"
        OCR = "ocr"

        # OTHERS_PANEL
        CONVERT = "convert"
        EXTRACT_IMG = "extract-img"
        REPAIR = "repair"

    def __init__(self, group_name: str, rich_help_panel: str) -> None:
        super().__init__(
            group_name=group_name,
            help=_("PDF file manipulation"),
            rich_help_panel=rich_help_panel,
        )

        # add subcommands
        self.add(
            # SECURITY_PANEL
            PdfEncryptCLI(
                group_name=group_name,
                command_name=self.Commands.ENCRYPT.value,
                rich_help_panel=self.Panels.SECURITY.value,
            ),
            PdfDecryptCLI(
                group_name=group_name,
                command_name=self.Commands.DECRYPT.value,
                rich_help_panel=self.Panels.SECURITY.value,
            ),

            # TRANSFORMATION_PANEL
            PdfCompressCLI(
                group_name=group_name,
                command_name=self.Commands.COMPRESS.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            PdfExtractCLI(
                group_name=group_name,
                command_name=self.Commands.EXTRACT.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            PdfMergeCLI(
                group_name=group_name,
                command_name=self.Commands.MERGE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            PdfRotateCLI(
                group_name=group_name,
                command_name=self.Commands.ROTATE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            PdfSplitCLI(
                group_name=group_name,
                command_name=self.Commands.SPLIT.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            PdfOcrCLI(
                group_name=group_name,
                command_name=self.Commands.OCR.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),

            # OTHERS_PANEL
            PdfConvertCLI(
                group_name=group_name,
                command_name=self.Commands.CONVERT.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),
            PdfExtractImgCLI(
                group_name=group_name,
                command_name=self.Commands.EXTRACT_IMG.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),
            PdfRepairCLI(
                group_name=group_name,
                command_name=self.Commands.REPAIR.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),
        )


__all__ = [
    "PdfTyperGroup",
]
