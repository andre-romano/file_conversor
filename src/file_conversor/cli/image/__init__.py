# src\file_conversor\cli\image\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils.abstract_typer_group import AbstractTyperGroup
from file_conversor.config.locale import get_translation

from file_conversor.cli.image.antialias_cmd import ImageAntialiasTyperCommand
from file_conversor.cli.image.blur_cmd import ImageBlurTyperCommand
from file_conversor.cli.image.compress_cmd import ImageCompressTyperCommand
from file_conversor.cli.image.convert_cmd import ImageConvertTyperCommand
from file_conversor.cli.image.filter_cmd import ImageFilterTyperCommand
from file_conversor.cli.image.enhance_cmd import ImageEnhanceTyperCommand
from file_conversor.cli.image.info_cmd import ImageInfoTyperCommand
from file_conversor.cli.image.mirror_cmd import ImageMirrorTyperCommand
from file_conversor.cli.image.render_cmd import ImageRenderTyperCommand
from file_conversor.cli.image.resize_cmd import ImageResizeTyperCommand
from file_conversor.cli.image.rotate_cmd import ImageRotateTyperCommand
from file_conversor.cli.image.to_pdf_cmd import ImageToPdfTyperCommand
from file_conversor.cli.image.unsharp_cmd import ImageUnsharpTyperCommand

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
            ImageConvertTyperCommand(
                group_name=group_name,
                command_name=self.Commands.CONVERT.value,
                rich_help_panel=self.Panels.CONVERSION.value,
            ),
            ImageRenderTyperCommand(
                group_name=group_name,
                command_name=self.Commands.RENDER.value,
                rich_help_panel=self.Panels.CONVERSION.value,
            ),
            ImageToPdfTyperCommand(
                group_name=group_name,
                command_name=self.Commands.TO_PDF.value,
                rich_help_panel=self.Panels.CONVERSION.value,
            ),

            # TRANSFORMATION
            ImageCompressTyperCommand(
                group_name=group_name,
                command_name=self.Commands.COMPRESS.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            ImageMirrorTyperCommand(
                group_name=group_name,
                command_name=self.Commands.MIRROR.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            ImageRotateTyperCommand(
                group_name=group_name,
                command_name=self.Commands.ROTATE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            ImageResizeTyperCommand(
                group_name=group_name,
                command_name=self.Commands.RESIZE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),

            # FILTER
            ImageAntialiasTyperCommand(
                group_name=group_name,
                command_name=self.Commands.ANTIALIAS.value,
                rich_help_panel=self.Panels.FILTER.value,
            ),
            ImageBlurTyperCommand(
                group_name=group_name,
                command_name=self.Commands.BLUR.value,
                rich_help_panel=self.Panels.FILTER.value,
            ),
            ImageEnhanceTyperCommand(
                group_name=group_name,
                command_name=self.Commands.ENHANCE.value,
                rich_help_panel=self.Panels.FILTER.value,
            ),
            ImageFilterTyperCommand(
                group_name=group_name,
                command_name=self.Commands.FILTER.value,
                rich_help_panel=self.Panels.FILTER.value,
            ),
            ImageUnsharpTyperCommand(
                group_name=group_name,
                command_name=self.Commands.UNSHARP.value,
                rich_help_panel=self.Panels.FILTER.value,
            ),

            # OTHERS
            ImageInfoTyperCommand(
                group_name=group_name,
                command_name=self.Commands.INFO.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),
        )


__all__ = [
    "ImageTyperGroup",
]
