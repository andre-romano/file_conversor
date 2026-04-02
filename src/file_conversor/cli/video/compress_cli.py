
# src\file_conversor\cli\video\compress_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
    TargetFileSizeOption,
    VideoEncodingSpeedOption,
    VideoProfileOption,
    VideoQualityOption,
)
from file_conversor.command.video import (
    VideoCompressCommand,
    VideoCompressEncoding,
    VideoCompressOutFormats,
    VideoCompressProfile,
    VideoCompressQuality,
)
from file_conversor.config import (
    Configuration,
    Log,
    State,
    get_translation,
)
from file_conversor.system import ContextMenu, ContextMenuItem


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoCompressCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        for ext_in in VideoCompressCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="compress",
                    description="Compress",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / "compress.ico",
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.compress,
            help=f"""
    {_('Compress a video file to a target file size.')}

    {_('Outputs an video file with _compressed at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.avi -od D:/Downloads --target-size 30M`

    - `file_conversor {group_name} {command_name} input_file1.mp4 -ts 50M`
""")

    def compress(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(VideoCompressCommand.get_in_formats())],

        target_size: Annotated[str, TargetFileSizeOption(prompt=f"{_("Target file size (size[K|M|G]) [0 = do not limit output file size]")}")],

        file_format: Annotated[VideoCompressOutFormats, FormatOption()] = VideoCompressOutFormats(CONFIG.video_format),

        video_profile: Annotated[VideoCompressProfile, VideoProfileOption()] = VideoCompressProfile(CONFIG.video_profile),
        video_encoding_speed: Annotated[VideoCompressEncoding, VideoEncodingSpeedOption()] = VideoCompressEncoding(CONFIG.video_encoding_speed),
        video_quality: Annotated[VideoCompressQuality, VideoQualityOption()] = VideoCompressQuality(CONFIG.video_quality),

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = VideoCompressCommand(
                input_files=input_files,
                target_size=target_size,
                video_profile=video_profile,
                video_encoding_speed=video_encoding_speed,
                video_quality=video_quality,
                file_format=file_format,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "VideoCompressCLI",
]
