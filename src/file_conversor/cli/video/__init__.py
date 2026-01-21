
# src\file_conversor\cli\video\__init__.py

from enum import Enum

# user-provided modules
from file_conversor.cli._utils.abstract_typer_group import AbstractTyperGroup

from file_conversor.cli.video.check_cmd import VideoCheckTyperCommand
from file_conversor.cli.video.compress_cmd import VideoCompressTyperCommand
from file_conversor.cli.video.convert_cmd import VideoConvertTyperCommand
from file_conversor.cli.video.enhance_cmd import VideoEnhanceTyperCommand
from file_conversor.cli.video.execute_cmd import VideoExecuteTyperCommand
from file_conversor.cli.video.info_cmd import VideoInfoTyperCommand
from file_conversor.cli.video.list_formats_cmd import VideoListFormatsTyperCommand
from file_conversor.cli.video.mirror_cmd import VideoMirrorTyperCommand
from file_conversor.cli.video.resize_cmd import VideoResizeTyperCommand
from file_conversor.cli.video.rotate_cmd import VideoRotateTyperCommand

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
            VideoConvertTyperCommand(
                group_name=group_name,
                command_name=self.Commands.CONVERT.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            VideoCompressTyperCommand(
                group_name=group_name,
                command_name=self.Commands.COMPRESS.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            VideoEnhanceTyperCommand(
                group_name=group_name,
                command_name=self.Commands.ENHANCE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            VideoMirrorTyperCommand(
                group_name=group_name,
                command_name=self.Commands.MIRROR.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            VideoRotateTyperCommand(
                group_name=group_name,
                command_name=self.Commands.ROTATE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),
            VideoResizeTyperCommand(
                group_name=group_name,
                command_name=self.Commands.RESIZE.value,
                rich_help_panel=self.Panels.TRANSFORMATION.value,
            ),

            # OTHERS_PANEL
            VideoCheckTyperCommand(
                group_name=group_name,
                command_name=self.Commands.CHECK.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),
            VideoInfoTyperCommand(
                group_name=group_name,
                command_name=self.Commands.INFO.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),
            VideoListFormatsTyperCommand(
                group_name=group_name,
                command_name=self.Commands.LIST_FORMATS.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),
            VideoExecuteTyperCommand(
                group_name=group_name,
                command_name=self.Commands.EXECUTE.value,
                rich_help_panel=self.Panels.OTHERS.value,
            ),
        )


__all__ = [
    "VideoTyperGroup",
]
