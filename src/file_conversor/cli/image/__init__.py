# src\file_conversor\cli\image\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils.abstract_typer_group import AbstractTyperGroup
from file_conversor.cli.image.antialias_cli import ImageAntialiasCLI
from file_conversor.cli.image.blur_cli import ImageBlurCLI
from file_conversor.cli.image.compress_cli import ImageCompressCLI
from file_conversor.cli.image.convert_cli import ImageConvertCLI
from file_conversor.cli.image.enhance_cli import ImageEnhanceCLI
from file_conversor.cli.image.filter_cli import ImageFilterCLI
from file_conversor.cli.image.info_cli import ImageInfoCLI
from file_conversor.cli.image.mirror_cli import ImageMirrorCLI
from file_conversor.cli.image.render_cli import ImageRenderCLI
from file_conversor.cli.image.resize_cli import ImageResizeCLI
from file_conversor.cli.image.rotate_cli import ImageRotateCLI
from file_conversor.cli.image.to_pdf_cli import ImageToPdfCLI
from file_conversor.cli.image.unsharp_cli import ImageUnsharpCLI
from file_conversor.config.locale import get_translation


_ = get_translation()


class ImageTyperGroup(AbstractTyperGroup):

    class Panels(Enum):
        CONVERSION = _("Conversions")
        TRANSFORMATION = _("Transformations")
        FILTER = _("Filters")
        OTHERS = _("Other commands")

    class Commands(Enum):
        # CONVERSION
        CONVERT = "convert"
        RENDER = "render"
        TO_PDF = "to-pdf"

        # TRANSFORMATION
        COMPRESS = "compress"
        MIRROR = "mirror"
        ROTATE = "rotate"
        RESIZE = "resize"

        # FILTER
        ANTIALIAS = "antialias"
        BLUR = "blur"
        ENHANCE = "enhance"
        FILTER = "filter"
        UNSHARP = "unsharp"

        # OTHERS
        INFO = "info"

    def __init__(self, group_name: str, rich_help_panel: str) -> None:
        super().__init__(
            group_name=group_name,
            help=_("Image file manipulation"),
            rich_help_panel=rich_help_panel,
        )

        # add subcommands
        self.add(
            # CONVERSION
            ImageConvertCLI(
                group_name=group_name,
                command_name=self.Commands.CONVERT.value,
                rich_help_panel=self.Panels.CONVERSION.value,
            ),
            ImageRenderCLI(
                group_name=group_name,
                command_name=self.Commands.RENDER.value,
                rich_help_panel=self.Panels.CONVERSION.value,
            ),
            ImageToPdfCLI(
                group_name=group_name,
                command_name=self.Commands.TO_PDF.value,
                rich_help_panel=self.Panels.CONVERSION.value,
            ),

            # TRANSFORMATION
            ImageCompressCLI(
                group_name=group_name,
                command_name=self.Commands.COMPRESS.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            ImageMirrorCLI(
                group_name=group_name,
                command_name=self.Commands.MIRROR.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            ImageRotateCLI(
                group_name=group_name,
                command_name=self.Commands.ROTATE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            ImageResizeCLI(
                group_name=group_name,
                command_name=self.Commands.RESIZE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),

            # FILTER
            ImageAntialiasCLI(
                group_name=group_name,
                command_name=self.Commands.ANTIALIAS.value,
                rich_help_panel=self.Panels.FILTER.value,
            ),
            ImageBlurCLI(
                group_name=group_name,
                command_name=self.Commands.BLUR.value,
                rich_help_panel=self.Panels.FILTER.value,
            ),
            ImageEnhanceCLI(
                group_name=group_name,
                command_name=self.Commands.ENHANCE.value,
                rich_help_panel=self.Panels.FILTER.value,
            ),
            ImageFilterCLI(
                group_name=group_name,
                command_name=self.Commands.FILTER.value,
                rich_help_panel=self.Panels.FILTER.value,
            ),
            ImageUnsharpCLI(
                group_name=group_name,
                command_name=self.Commands.UNSHARP.value,
                rich_help_panel=self.Panels.FILTER.value,
            ),

            # OTHERS
            ImageInfoCLI(
                group_name=group_name,
                command_name=self.Commands.INFO.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),
        )


__all__ = [
    "ImageTyperGroup",
]
