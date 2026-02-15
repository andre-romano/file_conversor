
# src\file_conversor\cli\video\convert_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    AudioBitrateOption,
    AudioCodecOption,
    AxisOption,
    BrightnessOption,
    ColorOption,
    ContrastOption,
    DeshakeOption,
    FormatOption,
    FPSOption,
    GammaOption,
    InputFilesArgument,
    OutputDirOption,
    ResolutionOption,
    UnsharpOption,
    VideoBitrateOption,
    VideoCodecOption,
    VideoEncodingSpeedOption,
    VideoProfileOption,
    VideoQualityOption,
    VideoRotationOption,
)
from file_conversor.command.video import VideoConvertCommand
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win import WinContextCommand, WinContextMenu
from file_conversor.utils.formatters import parse_ffmpeg_resolution


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoConvertCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = VideoConvertCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # FFMPEG commands
        icons_folder_path = Environment.get_icons_folder()
        for mode in VideoConvertCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="to_mkv",
                    description="To MKV",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f mkv "%1""',
                    icon=str(icons_folder_path / 'mkv.ico'),
                ),
                WinContextCommand(
                    name="to_mp4",
                    description="To MP4",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f mp4 "%1""',
                    icon=str(icons_folder_path / 'mp4.ico'),
                ),
                WinContextCommand(
                    name="to_webm",
                    description="To WEBM",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f webm "%1""',
                    icon=str(icons_folder_path / 'webm.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=_('Convert a video file to another video format.'),
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.webm -f mkv -od output_dir/ --audio-bitrate 192`

    - `file_conversor {group_name} {command_name} input_file.mp4 -f avi -r 90`

    - `file_conversor {group_name} {command_name} input_file.avi -f mp4 -rs 1280:720`
""")

    def convert(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in VideoConvertCommand.SupportedInFormats)],

        file_format: Annotated[VideoConvertCommand.SupportedOutFormats, FormatOption()] = VideoConvertCommand.SupportedOutFormats(CONFIG.video_format),

        audio_bitrate: Annotated[int | None, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int | None, VideoBitrateOption()] = CONFIG.video_bitrate,

        audio_codec: Annotated[VideoConvertCommand.AudioCodecs | None, AudioCodecOption()] = None,
        video_codec: Annotated[VideoConvertCommand.VideoCodecs | None, VideoCodecOption()] = None,

        video_profile: Annotated[VideoConvertCommand.VideoProfile, VideoProfileOption()] = VideoConvertCommand.VideoProfile(CONFIG.video_profile),
        video_encoding_speed: Annotated[VideoConvertCommand.VideoEncoding, VideoEncodingSpeedOption()] = VideoConvertCommand.VideoEncoding(CONFIG.video_encoding_speed),
        video_quality: Annotated[VideoConvertCommand.VideoQuality, VideoQualityOption()] = VideoConvertCommand.VideoQuality(CONFIG.video_quality),

        resolution: Annotated[str | None, ResolutionOption()] = None,
        fps: Annotated[int | None, FPSOption()] = None,

        brightness: Annotated[float, BrightnessOption()] = 1.0,
        contrast: Annotated[float, ContrastOption()] = 1.0,
        color: Annotated[float, ColorOption()] = 1.0,
        gamma: Annotated[float, GammaOption()] = 1.0,

        rotation: Annotated[VideoConvertCommand.Rotation | None, VideoRotationOption()] = None,
        mirror_axis: Annotated[VideoConvertCommand.MirrorAxis | None, AxisOption()] = None,

        deshake: Annotated[bool, DeshakeOption()] = False,
        unsharp: Annotated[bool, UnsharpOption()] = False,

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            VideoConvertCommand.convert(
                input_files=input_files,
                file_format=file_format,
                audio_bitrate=audio_bitrate,
                video_bitrate=video_bitrate,
                audio_codec=audio_codec,
                video_codec=video_codec,
                video_profile=video_profile,
                video_encoding_speed=video_encoding_speed,
                video_quality=video_quality,
                resolution=parse_ffmpeg_resolution(resolution),
                fps=fps,
                brightness=brightness,
                contrast=contrast,
                color=color,
                gamma=gamma,
                rotation=rotation,
                mirror_axis=mirror_axis,
                deshake=deshake,
                unsharp=unsharp,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "VideoConvertCLI",
]
