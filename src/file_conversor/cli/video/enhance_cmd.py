
# src\file_conversor\cli\video\enhance_cmd.py
from pathlib import Path
from typing import Annotated, Any, Callable, List, Iterable

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import AudioBitrateOption, BrightnessOption, ColorOption, ContrastOption, DeshakeOption, FPSOption, FormatOption, GammaOption, InputFilesArgument, OutputDirOption, ResolutionOption, UnsharpOption, VideoBitrateOption, VideoEncodingSpeedOption, VideoQualityOption

from file_conversor.cli.video._ffmpeg_cmd_helper import FFmpegCmdHelper

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils.validators import check_positive_integer, check_video_resolution, is_close, prompt_retry_on_exception

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoEnhanceTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = FFmpegCmdHelper.BACKEND.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # IMG2PDF commands
        for ext in FFmpegCmdHelper.BACKEND.SUPPORTED_IN_VIDEO_FORMATS:
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
        input_files: Annotated[List[Path], InputFilesArgument(FFmpegCmdHelper.BACKEND.SUPPORTED_IN_VIDEO_FORMATS)],

        file_format: Annotated[str, FormatOption(FFmpegCmdHelper.BACKEND.SUPPORTED_OUT_VIDEO_FORMATS)] = CONFIG.video_format,

        audio_bitrate: Annotated[int, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int, VideoBitrateOption()] = CONFIG.video_bitrate,

        video_encoding_speed: Annotated[str | None, VideoEncodingSpeedOption(FFmpegCmdHelper.BACKEND.ENCODING_SPEEDS)] = CONFIG.video_encoding_speed,
        video_quality: Annotated[str | None, VideoQualityOption(FFmpegCmdHelper.BACKEND.QUALITY_PRESETS)] = CONFIG.video_quality,
        resolution: Annotated[str | None, ResolutionOption()] = None,
        fps: Annotated[int | None, FPSOption()] = None,

        color: Annotated[float, ColorOption()] = 1.0,
        brightness: Annotated[float, BrightnessOption()] = 1.0,
        contrast: Annotated[float, ContrastOption()] = 1.0,
        gamma: Annotated[float, GammaOption()] = 1.0,

        deshake: Annotated[bool, DeshakeOption()] = False,
        unsharp: Annotated[bool, UnsharpOption()] = False,

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        if (not resolution
                and not fps
                and is_close(color, 1.0)
                and is_close(brightness, 1.0)
                and is_close(contrast, 1.0)
                and is_close(gamma, 1.0)
                and not deshake
                and not unsharp):
            resolution = prompt_retry_on_exception(
                text=f"{_("Target Resolution (width:height) [0:0 = do not change video resolution]")}",
                default="0:0", type=str, check_callback=check_video_resolution,
            )
            resolution = None if resolution == "0:0" else resolution

            fps = prompt_retry_on_exception(
                text=f"{_("Target FPS [0 = do not change FPS]")}",
                default=0, type=int, check_callback=check_positive_integer,
            )
            fps = None if fps is None or fps == 0 else fps

            color = prompt_retry_on_exception(
                text=f"{_("Color adjustment (> 1.0 increases color, < 1.0 decreases color)")}",
                default=1.0, type=float,
            )
            brightness = prompt_retry_on_exception(
                text=f"{_("Brightness adjustment (> 1.0 increases brightness, < 1.0 decreases brightness)")}",
                default=1.0, type=float,
            )
            contrast = prompt_retry_on_exception(
                text=f"{_("Contrast adjustment (> 1.0 increases contrast, < 1.0 decreases contrast)")}",
                default=1.0, type=float,
            )
            gamma = prompt_retry_on_exception(
                text=f"{_("Gamma adjustment (> 1.0 increases gamma, < 1.0 decreases gamma)")}",
                default=1.0, type=float,
            )

            deshake = prompt_retry_on_exception(
                text=f"{_('Apply deshake filter?')}",
                default=False, type=bool,
            )
            unsharp = prompt_retry_on_exception(
                text=f"{_('Apply unsharp filter?')}",
                default=False, type=bool,
            )

        ffmpeg_cmd_helper = FFmpegCmdHelper(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
            overwrite_output=STATE.overwrite_output.enabled,
        )

        # Set arguments for FFmpeg command helper
        ffmpeg_cmd_helper.set_input(input_files)
        ffmpeg_cmd_helper.set_output(file_format=file_format, out_stem="_enhanced", output_dir=output_dir)

        ffmpeg_cmd_helper.set_video_settings(encoding_speed=video_encoding_speed, quality=video_quality)
        ffmpeg_cmd_helper.set_bitrate(audio_bitrate=audio_bitrate, video_bitrate=video_bitrate)

        ffmpeg_cmd_helper.set_resolution_filter(resolution)
        ffmpeg_cmd_helper.set_fps_filter(fps)
        ffmpeg_cmd_helper.set_enhancement_filters(
            brightness=brightness,
            contrast=contrast,
            color=color,
            gamma=gamma,
        )
        ffmpeg_cmd_helper.set_deshake_filter(deshake)
        ffmpeg_cmd_helper.set_unsharp_filter(unsharp)

        ffmpeg_cmd_helper.execute()


__all__ = [
    "VideoEnhanceTyperCommand",
]
