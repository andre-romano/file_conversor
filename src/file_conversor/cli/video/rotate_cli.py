
# src\file_conversor\cli\video\rotate_cmd.py

from pathlib import Path
from typing import Annotated

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
from file_conversor.command.video import VideoRotateCommand
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win import WinContextCommand, WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoRotateCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = VideoRotateCommand.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # FFMPEG commands
        icons_folder_path = Environment.get_icons_folder()
        for mode in VideoRotateCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="rotate_anticlock_90",
                    description="Rotate Left",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -r -90"',
                    icon=str(icons_folder_path / "rotate_left.ico"),
                ),
                WinContextCommand(
                    name="rotate_clock_90",
                    description="Rotate Right",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -r 90"',
                    icon=str(icons_folder_path / "rotate_right.ico"),
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
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in VideoRotateCommand.SupportedInFormats)],

        rotation: Annotated[VideoRotateCommand.Rotation, VideoRotationOption()],

        file_format: Annotated[VideoRotateCommand.SupportedOutFormats, FormatOption()] = VideoRotateCommand.SupportedOutFormats(CONFIG.video_format),

        audio_bitrate: Annotated[int | None, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int | None, VideoBitrateOption()] = CONFIG.video_bitrate,

        video_profile: Annotated[VideoRotateCommand.VideoProfile, VideoProfileOption()] = VideoRotateCommand.VideoProfile(CONFIG.video_profile),
        video_encoding_speed: Annotated[VideoRotateCommand.VideoEncoding, VideoEncodingSpeedOption()] = VideoRotateCommand.VideoEncoding(CONFIG.video_encoding_speed),
        video_quality: Annotated[VideoRotateCommand.VideoQuality, VideoQualityOption()] = VideoRotateCommand.VideoQuality(CONFIG.video_quality),

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            VideoRotateCommand.rotate(
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


__all__ = [
    "VideoRotateCLI",
]
