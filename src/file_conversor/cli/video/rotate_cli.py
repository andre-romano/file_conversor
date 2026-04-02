
# src\file_conversor\cli\video\rotate_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    AudioBitrateOption,
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
    VideoBitrateOption,
    VideoEncodingSpeedOption,
    VideoProfileOption,
    VideoQualityOption,
    VideoRotationOption,
)
from file_conversor.command.video import (
    VideoRotateCommand,
    VideoRotateEncoding,
    VideoRotateOutFormats,
    VideoRotateProfile,
    VideoRotateQuality,
    VideoRotateRotation,
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


class VideoRotateCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path) -> None:
        # FFMPEG commands
        for ext_in in VideoRotateCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="rotate_anticlock_90",
                    description="Rotate Left",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-r", "-90"],
                    icon=icons_folder / "rotate_left.ico",
                ),
                ContextMenuItem(
                    name="rotate_clock_90",
                    description="Rotate Right",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-r", "90"],
                    icon=icons_folder / "rotate_right.ico",
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.rotate,
            help=f"""
    {_('Rotate a video file (clockwise or anti-clockwise).')}

    {_('Outputs an video file with _rotated at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.webm -r 90 -od output_dir/ --audio-bitrate 192`

    - `file_conversor {group_name} {command_name} input_file.mp4 -r 180`
""")

    def rotate(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(VideoRotateCommand.get_in_formats())],

        rotation: Annotated[VideoRotateRotation, VideoRotationOption()],

        file_format: Annotated[VideoRotateOutFormats, FormatOption()] = VideoRotateOutFormats(CONFIG.video_format),

        audio_bitrate: Annotated[int | None, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int | None, VideoBitrateOption()] = CONFIG.video_bitrate,

        video_profile: Annotated[VideoRotateProfile, VideoProfileOption()] = VideoRotateProfile(CONFIG.video_profile),
        video_encoding_speed: Annotated[VideoRotateEncoding, VideoEncodingSpeedOption()] = VideoRotateEncoding(CONFIG.video_encoding_speed),
        video_quality: Annotated[VideoRotateQuality, VideoQualityOption()] = VideoRotateQuality(CONFIG.video_quality),

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = VideoRotateCommand(
                input_files=input_files,
                rotation=rotation,
                file_format=file_format,
                audio_bitrate=audio_bitrate,
                video_bitrate=video_bitrate,
                video_profile=video_profile,
                video_encoding_speed=video_encoding_speed,
                video_quality=video_quality,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "VideoRotateCLI",
]
