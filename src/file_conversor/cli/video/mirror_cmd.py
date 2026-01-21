
# src\file_conversor\cli\video\mirror_cmd.py

from typing import Annotated, Any, Callable, Iterable, List
from pathlib import Path

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import (
    AudioBitrateOption, AxisOption, FormatOption, InputFilesArgument,
    OutputDirOption, VideoBitrateOption, VideoEncodingSpeedOption,
    VideoQualityOption,
)

from file_conversor.cli.video._ffmpeg_cmd_helper import FFmpegCmdHelper

from file_conversor.backend import FFmpegBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoMirrorTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        icons_folder_path = Environment.get_icons_folder()
        for ext in FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="mirror_x",
                    description="Mirror X axis",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -a x"',
                    icon=str(icons_folder_path / "left_right.ico"),
                ),
                WinContextCommand(
                    name="mirror_y",
                    description="Mirror Y axis",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -a y"',
                    icon=str(icons_folder_path / "up_down.ico"),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.mirror,
            help=f"""
    {_('Mirror a video file (vertically or horizontally).')}

    {_('Outputs a video file with _mirrored at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.webm -a x -od output_dir/ --audio-bitrate 192`

    - `file_conversor {group_name} {command_name} input_file.mp4 -a y`
""")

    def mirror(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS)],

        mirror_axis: Annotated[str, AxisOption()],

        file_format: Annotated[str, FormatOption(FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS)] = CONFIG.video_format,

        audio_bitrate: Annotated[int, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int, VideoBitrateOption()] = CONFIG.video_bitrate,

        video_encoding_speed: Annotated[str | None, VideoEncodingSpeedOption(FFmpegBackend.ENCODING_SPEEDS)] = CONFIG.video_encoding_speed,
        video_quality: Annotated[str | None, VideoQualityOption(FFmpegBackend.QUALITY_PRESETS)] = CONFIG.video_quality,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        ffmpeg_cmd_helper = FFmpegCmdHelper(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
            overwrite_output=STATE.overwrite_output.enabled,
        )

        # Set arguments for FFmpeg command helper
        ffmpeg_cmd_helper.set_input(input_files)
        ffmpeg_cmd_helper.set_output(file_format=file_format, out_stem="_mirrored", output_dir=output_dir)

        ffmpeg_cmd_helper.set_video_settings(encoding_speed=video_encoding_speed, quality=video_quality)
        ffmpeg_cmd_helper.set_bitrate(audio_bitrate=audio_bitrate, video_bitrate=video_bitrate)
        ffmpeg_cmd_helper.set_mirror_filter(mirror_axis)

        ffmpeg_cmd_helper.execute()


__all__ = [
    "VideoMirrorTyperCommand",
]
