
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
    HeightOption,
    InputFilesArgument,
    OutputDirOption,
    UnsharpOption,
    VideoBitrateOption,
    VideoCodecOption,
    VideoEncodingSpeedOption,
    VideoProfileOption,
    VideoQualityOption,
    VideoRotationOption,
    WidthOption,
)
from file_conversor.command.video import (
    VideoConvertAudioCodecs,
    VideoConvertCommand,
    VideoConvertEncoding,
    VideoConvertMirrorAxis,
    VideoConvertOutFormats,
    VideoConvertProfile,
    VideoConvertQuality,
    VideoConvertRotation,
    VideoConvertVideoCodecs,
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


class VideoConvertCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        # FFMPEG commands
        for ext_in in VideoConvertCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name=f"to_{ext_out}",
                    description=f"To {ext_out.upper()}",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-f", ext_out],
                    icon=icons_folder / f"{ext_out}.ico",
                )
                for ext_out in ["mkv", "mp4", "webm"]
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

    - `file_conversor {group_name} {command_name} input_file.avi -f mp4 -w 1280 -h 720`
""")

    def convert(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(VideoConvertCommand.get_in_formats())],

        file_format: Annotated[VideoConvertOutFormats, FormatOption()] = VideoConvertOutFormats(CONFIG.video_format),

        audio_bitrate: Annotated[int | None, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int | None, VideoBitrateOption()] = CONFIG.video_bitrate,

        audio_codec: Annotated[VideoConvertAudioCodecs | None, AudioCodecOption()] = None,
        video_codec: Annotated[VideoConvertVideoCodecs | None, VideoCodecOption()] = None,

        video_profile: Annotated[VideoConvertProfile, VideoProfileOption()] = VideoConvertProfile(CONFIG.video_profile),
        video_encoding_speed: Annotated[VideoConvertEncoding, VideoEncodingSpeedOption()] = VideoConvertEncoding(CONFIG.video_encoding_speed),
        video_quality: Annotated[VideoConvertQuality, VideoQualityOption()] = VideoConvertQuality(CONFIG.video_quality),

        width: Annotated[int | None, WidthOption()] = None,
        height: Annotated[int | None, HeightOption()] = None,
        fps: Annotated[int | None, FPSOption()] = None,

        brightness: Annotated[float, BrightnessOption()] = 1.0,
        contrast: Annotated[float, ContrastOption()] = 1.0,
        color: Annotated[float, ColorOption()] = 1.0,
        gamma: Annotated[float, GammaOption()] = 1.0,

        rotation: Annotated[VideoConvertRotation | None, VideoRotationOption()] = None,
        mirror_axis: Annotated[VideoConvertMirrorAxis | None, AxisOption()] = None,

        deshake: Annotated[bool, DeshakeOption()] = False,
        unsharp: Annotated[bool, UnsharpOption()] = False,

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = VideoConvertCommand(
                input_files=input_files,
                file_format=file_format,
                audio_bitrate=audio_bitrate,
                video_bitrate=video_bitrate,
                audio_codec=audio_codec,
                video_codec=video_codec,
                video_profile=video_profile,
                video_encoding_speed=video_encoding_speed,
                video_quality=video_quality,
                width=width,
                height=height,
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
            command.execute()


__all__ = [
    "VideoConvertCLI",
]
