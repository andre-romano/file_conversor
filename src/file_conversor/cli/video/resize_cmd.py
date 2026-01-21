
# src\file_conversor\cli\video\resize_cmd.py

from typing import Annotated, Any, Callable, List, Iterable
from pathlib import Path

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import AudioBitrateOption, FormatOption, InputFilesArgument, OutputDirOption, ResolutionOption, VideoBitrateOption, VideoEncodingSpeedOption, VideoQualityOption

from file_conversor.cli.video._ffmpeg_cmd_helper import FFmpegCmdHelper

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoResizeTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = FFmpegCmdHelper.BACKEND.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        icons_folder_path = Environment.get_icons_folder()
        for ext in FFmpegCmdHelper.BACKEND.SUPPORTED_IN_VIDEO_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="resize",
                    description="Resize",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / "resize.ico"),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.resize,
            help=f"""
    {_('Resize a video file (downscaling / upscaling).')}

    {_('Outputs a video file with _resized at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.webm -rs 1024:768 -od output_dir/ -f mp4 --audio-bitrate 192`

    - `file_conversor {group_name} {command_name} input_file.mp4 -rs 1280:720`
""")

    def resize(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(FFmpegCmdHelper.BACKEND.SUPPORTED_IN_VIDEO_FORMATS)],

        resolution: Annotated[str, ResolutionOption(prompt=f"{_('Enter target resolution (WIDTH:HEIGHT)')}")],

        file_format: Annotated[str, FormatOption(FFmpegCmdHelper.BACKEND.SUPPORTED_OUT_VIDEO_FORMATS)] = CONFIG.video_format,

        audio_bitrate: Annotated[int, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int, VideoBitrateOption()] = CONFIG.video_bitrate,

        video_encoding_speed: Annotated[str | None, VideoEncodingSpeedOption(FFmpegCmdHelper.BACKEND.ENCODING_SPEEDS)] = CONFIG.video_encoding_speed,
        video_quality: Annotated[str | None, VideoQualityOption(FFmpegCmdHelper.BACKEND.QUALITY_PRESETS)] = CONFIG.video_quality,

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        ffmpeg_cmd_helper = FFmpegCmdHelper(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
            overwrite_output=STATE.overwrite_output.enabled,
        )

        # Set arguments for FFmpeg command helper
        ffmpeg_cmd_helper.set_input(input_files)
        ffmpeg_cmd_helper.set_output(file_format=file_format, out_stem="_resized", output_dir=output_dir)

        ffmpeg_cmd_helper.set_video_settings(encoding_speed=video_encoding_speed, quality=video_quality)
        ffmpeg_cmd_helper.set_bitrate(audio_bitrate=audio_bitrate, video_bitrate=video_bitrate)
        ffmpeg_cmd_helper.set_resolution_filter(resolution)

        ffmpeg_cmd_helper.execute()


__all__ = [
    "VideoResizeTyperCommand",
]
