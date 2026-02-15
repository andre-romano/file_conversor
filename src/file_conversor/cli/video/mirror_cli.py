
# src\file_conversor\cli\video\mirror_cmd.py

from pathlib import Path
from typing import Annotated

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    AudioBitrateOption,
    AxisOption,
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
    VideoBitrateOption,
    VideoEncodingSpeedOption,
    VideoProfileOption,
    VideoQualityOption,
)
from file_conversor.command.video import VideoMirrorCommand
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


class VideoMirrorCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = VideoMirrorCommand.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        icons_folder_path = Environment.get_icons_folder()
        for mode in VideoMirrorCommand.SupportedInFormats:
            ext = mode.value
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
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in VideoMirrorCommand.SupportedInFormats)],

        mirror_axis: Annotated[VideoMirrorCommand.MirrorAxis, AxisOption()],

        file_format: Annotated[VideoMirrorCommand.SupportedOutFormats, FormatOption()] = VideoMirrorCommand.SupportedOutFormats(CONFIG.video_format),

        audio_bitrate: Annotated[int | None, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int | None, VideoBitrateOption()] = CONFIG.video_bitrate,

        video_profile: Annotated[VideoMirrorCommand.VideoProfile, VideoProfileOption()] = VideoMirrorCommand.VideoProfile(CONFIG.video_profile),
        video_encoding_speed: Annotated[VideoMirrorCommand.VideoEncoding, VideoEncodingSpeedOption()] = VideoMirrorCommand.VideoEncoding(CONFIG.video_encoding_speed),
        video_quality: Annotated[VideoMirrorCommand.VideoQuality, VideoQualityOption()] = VideoMirrorCommand.VideoQuality(CONFIG.video_quality),

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            VideoMirrorCommand.mirror(
                input_files=input_files,
                mirror_axis=mirror_axis,
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
    "VideoMirrorCLI",
]
