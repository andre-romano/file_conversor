# src\file_conversor\cli\pdf\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.config.locale import get_translation

from file_conversor.cli._utils.abstract_typer_group import AbstractTyperGroup

from file_conversor.cli.pdf.compress_cmd import PdfCompressTyperCommand
from file_conversor.cli.pdf.convert_cmd import PdfConvertTyperCommand
from file_conversor.cli.pdf.decrypt_cmd import PdfDecryptTyperCommand
from file_conversor.cli.pdf.encrypt_cmd import PdfEncryptTyperCommand
from file_conversor.cli.pdf.extract_cmd import PdfExtractTyperCommand
from file_conversor.cli.pdf.extract_img_cmd import PdfExtractImgTyperCommand
from file_conversor.cli.pdf.merge_cmd import PdfMergeTyperCommand
from file_conversor.cli.pdf.ocr_cmd import PdfOcrTyperCommand
from file_conversor.cli.pdf.repair_cmd import PdfRepairTyperCommand
from file_conversor.cli.pdf.rotate_cmd import PdfRotateTyperCommand
from file_conversor.cli.pdf.split_cmd import PdfSplitTyperCommand

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
            PdfEncryptTyperCommand(
                group_name=group_name,
                command_name=self.Commands.ENCRYPT.value,
                rich_help_panel=self.Panels.SECURITY.value,
            ),
            PdfDecryptTyperCommand(
                group_name=group_name,
                command_name=self.Commands.DECRYPT.value,
                rich_help_panel=self.Panels.SECURITY.value,
            ),

            # TRANSFORMATION_PANEL
            PdfCompressTyperCommand(
                group_name=group_name,
                command_name=self.Commands.COMPRESS.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            PdfExtractTyperCommand(
                group_name=group_name,
                command_name=self.Commands.EXTRACT.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            PdfMergeTyperCommand(
                group_name=group_name,
                command_name=self.Commands.MERGE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            PdfRotateTyperCommand(
                group_name=group_name,
                command_name=self.Commands.ROTATE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            PdfSplitTyperCommand(
                group_name=group_name,
                command_name=self.Commands.SPLIT.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            PdfOcrTyperCommand(
                group_name=group_name,
                command_name=self.Commands.OCR.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),

            # OTHERS_PANEL
            PdfConvertTyperCommand(
                group_name=group_name,
                command_name=self.Commands.CONVERT.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            PdfExtractImgTyperCommand(
                group_name=group_name,
                command_name=self.Commands.EXTRACT_IMG.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            PdfRepairTyperCommand(
                group_name=group_name,
                command_name=self.Commands.REPAIR.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
        )


__all__ = [
    "PdfTyperGroup",
]
