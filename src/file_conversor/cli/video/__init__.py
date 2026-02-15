
# src\file_conversor\cli\video\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils.abstract_typer_group import AbstractTyperGroup
from file_conversor.cli.video.check_cli import VideoCheckCLI
from file_conversor.cli.video.compress_cli import VideoCompressCLI
from file_conversor.cli.video.convert_cli import VideoConvertCLI
from file_conversor.cli.video.enhance_cli import VideoEnhanceCLI
from file_conversor.cli.video.execute_cli import VideoExecuteCLI
from file_conversor.cli.video.info_cli import VideoInfoCLI
from file_conversor.cli.video.list_formats_cli import VideoListFormatsCLI
from file_conversor.cli.video.mirror_cli import VideoMirrorCLI
from file_conversor.cli.video.resize_cli import VideoResizeCLI
from file_conversor.cli.video.rotate_cli import VideoRotateCLI
from file_conversor.config.locale import get_translation


_ = get_translation()


class VideoTyperGroup(AbstractTyperGroup):
    class Panels(Enum):
        TRANSFORMATION = _("Transformations")
        OTHERS = _("Other commands")

    class Commands(Enum):
        CHECK = "check"
        COMPRESS = "compress"
        CONVERT = "convert"
        ENHANCE = "enhance"
        EXECUTE = "execute"
        INFO = "info"
        LIST_FORMATS = "list-formats"
        MIRROR = "mirror"
        RESIZE = "resize"
        ROTATE = "rotate"

    def __init__(self, group_name: str, rich_help_panel: str) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            help=_("Video file manipulation (requires FFMpeg external library)"),
        )

        # add subcommands
        self.add(
            # TRANSFORMATION_PANEL
            VideoConvertCLI(
                group_name=group_name,
                command_name=self.Commands.CONVERT.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            VideoCompressCLI(
                group_name=group_name,
                command_name=self.Commands.COMPRESS.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            VideoEnhanceCLI(
                group_name=group_name,
                command_name=self.Commands.ENHANCE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            VideoMirrorCLI(
                group_name=group_name,
                command_name=self.Commands.MIRROR.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            VideoRotateCLI(
                group_name=group_name,
                command_name=self.Commands.ROTATE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            VideoResizeCLI(
                group_name=group_name,
                command_name=self.Commands.RESIZE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),

            # OTHERS_PANEL
            VideoCheckCLI(
                group_name=group_name,
                command_name=self.Commands.CHECK.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),
            VideoInfoCLI(
                group_name=group_name,
                command_name=self.Commands.INFO.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),
            VideoListFormatsCLI(
                group_name=group_name,
                command_name=self.Commands.LIST_FORMATS.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),
            VideoExecuteCLI(
                group_name=group_name,
                command_name=self.Commands.EXECUTE.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),
        )


__all__ = [
    "VideoTyperGroup",
]
