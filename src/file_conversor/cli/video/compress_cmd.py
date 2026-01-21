
# src\file_conversor\cli\video\compress_cmd.py

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import FormatOption, InputFilesArgument, OutputDirOption, TargetFileSizeOption, VideoEncodingSpeedOption, VideoQualityOption

from file_conversor.cli.video._ffmpeg_cmd_helper import FFmpegCmdHelper

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoCompressTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = FFmpegCmdHelper.BACKEND.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for ext in FFmpegCmdHelper.BACKEND.SUPPORTED_IN_VIDEO_FORMATS:
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
        input_files: Annotated[List[Path], InputFilesArgument(FFmpegCmdHelper.BACKEND.SUPPORTED_IN_VIDEO_FORMATS)],
        target_size: Annotated[str, TargetFileSizeOption(prompt=f"{_("Target file size (size[K|M|G]) [0 = do not limit output file size]")}")],
        video_encoding_speed: Annotated[str | None, VideoEncodingSpeedOption(FFmpegCmdHelper.BACKEND.ENCODING_SPEEDS)] = CONFIG.video_encoding_speed,
        video_quality: Annotated[str | None, VideoQualityOption(FFmpegCmdHelper.BACKEND.QUALITY_PRESETS)] = CONFIG.video_quality,
        file_format: Annotated[str, FormatOption(FFmpegCmdHelper.BACKEND.SUPPORTED_OUT_VIDEO_FORMATS)] = CONFIG.video_format,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        ffmpeg_cmd_helper = FFmpegCmdHelper(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
            overwrite_output=STATE.overwrite_output.enabled,
        )

        # Set arguments for FFmpeg command helper
        ffmpeg_cmd_helper.set_input(input_files)
        ffmpeg_cmd_helper.set_output(file_format=file_format, out_stem="_compressed", output_dir=output_dir)

        ffmpeg_cmd_helper.set_video_settings(encoding_speed=video_encoding_speed, quality=video_quality)
        ffmpeg_cmd_helper.set_target_size(target_size)

        ffmpeg_cmd_helper.execute()


__all__ = [
    "VideoCompressTyperCommand",
]
