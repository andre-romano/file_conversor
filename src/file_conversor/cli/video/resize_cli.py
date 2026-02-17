
# src\file_conversor\cli\video\resize_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    AudioBitrateOption,
    FormatOption,
    HeightOption,
    InputFilesArgument,
    OutputDirOption,
    VideoBitrateOption,
    VideoEncodingSpeedOption,
    VideoProfileOption,
    VideoQualityOption,
    WidthOption,
)
from file_conversor.command.video import VideoResizeCommand
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


class VideoResizeCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = VideoResizeCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        icons_folder_path = Environment.get_icons_folder()
        for mode in VideoResizeCommand.SupportedInFormats:
            ext = mode.value
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
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in VideoResizeCommand.SupportedInFormats)],

        width: Annotated[int, WidthOption(prompt=f"{_('Enter target width [pixels]')}")],
        height: Annotated[int, HeightOption(prompt=f"{_('Enter target height [pixels]')}")],

        file_format: Annotated[VideoResizeCommand.SupportedOutFormats, FormatOption()] = VideoResizeCommand.SupportedOutFormats(CONFIG.video_format),

        audio_bitrate: Annotated[int | None, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int | None, VideoBitrateOption()] = CONFIG.video_bitrate,

        video_profile: Annotated[VideoResizeCommand.VideoProfile, VideoProfileOption()] = VideoResizeCommand.VideoProfile(CONFIG.video_profile),
        video_encoding_speed: Annotated[VideoResizeCommand.VideoEncoding, VideoEncodingSpeedOption()] = VideoResizeCommand.VideoEncoding(CONFIG.video_encoding_speed),
        video_quality: Annotated[VideoResizeCommand.VideoQuality, VideoQualityOption()] = VideoResizeCommand.VideoQuality(CONFIG.video_quality),

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            VideoResizeCommand.resize(
                input_files=input_files,
                width=width,
                height=height,
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
    "VideoResizeCLI",
]
