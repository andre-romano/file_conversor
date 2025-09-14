
# src\file_conversor\cli\video\_ffmpeg_cmd.py

from rich import print

from typing import Annotated, Any, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend
from file_conversor.backend.audio_video.ffmpeg_filter import FFmpegFilter, FFmpegFilterDeshake, FFmpegFilterEq, FFmpegFilterHflip, FFmpegFilterMInterpolate, FFmpegFilterScale, FFmpegFilterTranspose, FFmpegFilterUnsharp, FFmpegFilterVflip

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.validators import check_valid_options
from file_conversor.utils.typer_utils import AudioBitrateOption, AudioCodecOption, AxisOption, BrightnessOption, ColorOption, ContrastOption, DeshakeOption, FPSOption, FormatOption, GammaOption, InputFilesArgument, OutputDirOption, ResolutionOption, UnsharpOption, VideoBitrateOption, VideoCodecOption, VideoRotationOption

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _ffmpeg_cli_cmd(  # pyright: ignore[reportUnusedFunction]
    input_files: List[Path],

    file_format: str,
    out_stem: str = "",

    audio_bitrate: int = 0,
    video_bitrate: int = 0,

    audio_codec: str | None = None,
    video_codec: str | None = None,

    resolution: str | None = None,
    fps: int | None = None,

    brightness: float = 1.0,
    contrast: float = 1.0,
    color: float = 1.0,
    gamma: float = 1.0,

    rotation: int | None = None,
    mirror_axis: str | None = None,
    deshake: bool = False,
    unsharp: bool = False,

    audio_codec_options: dict[str, Any] = {},
    video_codec_options: dict[str, Any] = {},

    output_dir: Path = Path(),
):
    # init ffmpeg
    ffmpeg_backend = FFmpegBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
        overwrite_output=STATE["overwrite-output"],
    )

    # set filters
    audio_filters: list[FFmpegFilter] = list()
    video_filters: list[FFmpegFilter] = list()

    if resolution is not None:
        video_filters.append(FFmpegFilterScale(*resolution.split(":")))

    if fps is not None:
        video_filters.append(FFmpegFilterMInterpolate(fps=fps))

    if brightness != 1.0 or contrast != 1.0 or color != 1.0 or gamma != 1.0:
        video_filters.append(FFmpegFilterEq(brightness=brightness, contrast=contrast, saturation=color, gamma=gamma))

    if rotation is not None:
        if rotation in (90, -90):
            direction = {90: 1, -90: 2}[rotation]
            video_filters.append(FFmpegFilterTranspose(direction=direction))
        else:
            video_filters.append(FFmpegFilterTranspose(direction=1))
            video_filters.append(FFmpegFilterTranspose(direction=1))

    if mirror_axis is not None:
        if mirror_axis == "x":
            video_filters.append(FFmpegFilterHflip())
        else:
            video_filters.append(FFmpegFilterVflip())

    if deshake:
        video_filters.append(FFmpegFilterDeshake())

    if unsharp:
        video_filters.append(FFmpegFilterUnsharp())

    two_pass = (video_bitrate > 0) or (audio_bitrate > 0)

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        ffmpeg_backend.set_files(input_file=input_file, output_file=output_file)
        ffmpeg_backend.set_audio_codec(codec=audio_codec, bitrate=audio_bitrate, filters=audio_filters, options=audio_codec_options)
        ffmpeg_backend.set_video_codec(codec=video_codec, bitrate=video_bitrate, filters=video_filters, options=video_codec_options)

        # display current progress
        process = ffmpeg_backend.execute(
            progress_callback=progress_mgr.update_progress,
            pass_num=1 if two_pass else 0,
        )
        progress_mgr.complete_step()

        if two_pass:
            # display current progress
            process = ffmpeg_backend.execute(
                progress_callback=progress_mgr.update_progress,
                pass_num=2,
            )
            progress_mgr.complete_step()

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, steps=2 if two_pass else 1, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_suffix=f".{file_format}", out_stem=out_stem)

    logger.info(f"{_('FFMpeg result')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
