
# src\file_conversor\cli\video\mirror_cmd.py

from pathlib import Path
from typing import Annotated, override

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
from file_conversor.command.video import (
    VideoMirrorAxis,
    VideoMirrorCommand,
    VideoMirrorEncoding,
    VideoMirrorOutFormats,
    VideoMirrorProfile,
    VideoMirrorQuality,
)
from file_conversor.config import CONFIG, LOG, STATE, get_translation
from file_conversor.system import ContextMenu, ContextMenuItem


_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoMirrorCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path) -> None:
        for ext_in in VideoMirrorCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="mirror_x",
                    description="Mirror X axis",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-a", "x"],
                    icon=icons_folder / "left_right.ico",
                ),
                ContextMenuItem(
                    name="mirror_y",
                    description="Mirror Y axis",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-a", "y"],
                    icon=icons_folder / "up_down.ico",
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
        input_files: Annotated[list[Path], InputFilesArgument(VideoMirrorCommand.get_in_formats())],

        mirror_axis: Annotated[VideoMirrorAxis, AxisOption()],

        file_format: Annotated[VideoMirrorOutFormats, FormatOption()] = VideoMirrorOutFormats(CONFIG.video_format),

        audio_bitrate: Annotated[int | None, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int | None, VideoBitrateOption()] = CONFIG.video_bitrate,

        video_profile: Annotated[VideoMirrorProfile, VideoProfileOption()] = VideoMirrorProfile(CONFIG.video_profile),
        video_encoding_speed: Annotated[VideoMirrorEncoding, VideoEncodingSpeedOption()] = VideoMirrorEncoding(CONFIG.video_encoding_speed),
        video_quality: Annotated[VideoMirrorQuality, VideoQualityOption()] = VideoMirrorQuality(CONFIG.video_quality),

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = VideoMirrorCommand(
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
            command.execute()


__all__ = [
    "VideoMirrorCLI",
]
