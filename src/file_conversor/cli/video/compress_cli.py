
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
from file_conversor.command.video import VideoCompressCommand
from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation
from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoCompressCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = VideoCompressCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for mode in VideoCompressCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="compress",
                    description="Compress",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / "compress.ico"),
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
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in VideoCompressCommand.SupportedInFormats)],

        target_size: Annotated[str, TargetFileSizeOption(prompt=f"{_("Target file size (size[K|M|G]) [0 = do not limit output file size]")}")],

        file_format: Annotated[VideoCompressCommand.SupportedOutFormats, FormatOption()] = VideoCompressCommand.SupportedOutFormats(CONFIG.video_format),

        video_profile: Annotated[VideoCompressCommand.VideoProfile, VideoProfileOption()] = VideoCompressCommand.VideoProfile(CONFIG.video_profile),
        video_encoding_speed: Annotated[VideoCompressCommand.VideoEncoding, VideoEncodingSpeedOption()] = VideoCompressCommand.VideoEncoding(CONFIG.video_encoding_speed),
        video_quality: Annotated[VideoCompressCommand.VideoQuality, VideoQualityOption()] = VideoCompressCommand.VideoQuality(CONFIG.video_quality),

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            VideoCompressCommand.compress(
                input_files=input_files,
                target_size=target_size,
                video_profile=video_profile,
                video_encoding_speed=video_encoding_speed,
                video_quality=video_quality,
                file_format=file_format,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "VideoCompressCLI",
]
