
# src\file_conversor\cli\video\enhance_cmd.py
from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    AudioBitrateOption,
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
    VideoEncodingSpeedOption,
    VideoProfileOption,
    VideoQualityOption,
)
from file_conversor.command.video import VideoEnhanceCommand
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu
from file_conversor.utils.formatters import parse_ffmpeg_resolution
from file_conversor.utils.validators import (
    check_video_resolution,
    is_close,
    prompt_retry_on_exception,
)


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoEnhanceCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = VideoEnhanceCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for mode in VideoEnhanceCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="enhance",
                    description="Enhance",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / "color.ico"),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.enhance,
            help=f"""
        {_('Enhance video bitrate, resolution, fps, color, brightness, etc.')}
    """,
            epilog=f"""
        **{_('Examples')}:**

        - `file_conversor {group_name} {command_name} input_file.avi -od D:/Downloads --color 1.20`

        - `file_conversor {group_name} {command_name} input_file1.mp4 --unsharp`

        - `file_conversor {group_name} {command_name} input_file.mkv -cl 0.85 -b 1.10`        
    """)

    def enhance(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in VideoEnhanceCommand.SupportedInFormats)],

        file_format: Annotated[VideoEnhanceCommand.SupportedOutFormats, FormatOption()] = VideoEnhanceCommand.SupportedOutFormats(CONFIG.video_format),

        audio_bitrate: Annotated[int | None, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int | None, VideoBitrateOption()] = CONFIG.video_bitrate,

        video_profile: Annotated[VideoEnhanceCommand.VideoProfile, VideoProfileOption()] = VideoEnhanceCommand.VideoProfile(CONFIG.video_profile),
        video_encoding_speed: Annotated[VideoEnhanceCommand.VideoEncoding, VideoEncodingSpeedOption()] = VideoEnhanceCommand.VideoEncoding(CONFIG.video_encoding_speed),
        video_quality: Annotated[VideoEnhanceCommand.VideoQuality, VideoQualityOption()] = VideoEnhanceCommand.VideoQuality(CONFIG.video_quality),

        resolution: Annotated[str | None, ResolutionOption()] = None,
        fps: Annotated[int | None, FPSOption()] = None,

        brightness: Annotated[float, BrightnessOption()] = 1.0,
        contrast: Annotated[float, ContrastOption()] = 1.0,
        color: Annotated[float, ColorOption()] = 1.0,
        gamma: Annotated[float, GammaOption()] = 1.0,

        deshake: Annotated[bool, DeshakeOption()] = False,
        unsharp: Annotated[bool, UnsharpOption()] = False,

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        if (
            all(x is None for x in (resolution, fps))
            and all(is_close(x, 1.0) for x in (color, brightness, contrast, gamma))
            and all(x == False for x in (deshake, unsharp))
        ):
            resolution = prompt_retry_on_exception(
                text=f"{_("Target Resolution (width:height) [0:0 = do not change video resolution]")}",
                default="0:0", type=str,
                check_callback=check_video_resolution,
            )

            fps = prompt_retry_on_exception(
                text=f"{_("Target FPS [0 = do not change FPS]")}",
                default=0, type=int,
                check_callback=lambda x: x >= 0,
            )

            color = prompt_retry_on_exception(
                text=f"{_("Color adjustment (> 1.0 increases color, < 1.0 decreases color)")}",
                default=1.0, type=float,
                check_callback=lambda x: x >= 0,
            )
            brightness = prompt_retry_on_exception(
                text=f"{_("Brightness adjustment (> 1.0 increases brightness, < 1.0 decreases brightness)")}",
                default=1.0, type=float,
                check_callback=lambda x: x >= 0,
            )
            contrast = prompt_retry_on_exception(
                text=f"{_("Contrast adjustment (> 1.0 increases contrast, < 1.0 decreases contrast)")}",
                default=1.0, type=float,
                check_callback=lambda x: x >= 0,
            )
            gamma = prompt_retry_on_exception(
                text=f"{_("Gamma adjustment (> 1.0 increases gamma, < 1.0 decreases gamma)")}",
                default=1.0, type=float,
                check_callback=lambda x: x >= 0,
            )

            deshake = prompt_retry_on_exception(
                text=f"{_('Apply deshake filter?')}",
                default=False, type=bool,
            )
            unsharp = prompt_retry_on_exception(
                text=f"{_('Apply unsharp filter?')}",
                default=False, type=bool,
            )
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            VideoEnhanceCommand.enhance(
                input_files=input_files,
                file_format=file_format,
                audio_bitrate=audio_bitrate,
                video_bitrate=video_bitrate,
                video_profile=video_profile,
                video_encoding_speed=video_encoding_speed,
                video_quality=video_quality,
                resolution=parse_ffmpeg_resolution(resolution),
                fps=fps,
                brightness=brightness,
                contrast=contrast,
                color=color,
                gamma=gamma,
                deshake=deshake,
                unsharp=unsharp,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "VideoEnhanceCLI",
]
