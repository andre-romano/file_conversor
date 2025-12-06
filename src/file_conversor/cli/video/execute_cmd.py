
# src\file_conversor\cli\video\execute_cmd.py

import shlex
import typer

from rich import print

from typing import Annotated, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend
from file_conversor.backend.audio_video.ffmpeg_filter import FFmpegFilter

from file_conversor.cli.video._typer import OTHERS_PANEL as RICH_HELP_PANEL
from file_conversor.cli.video._typer import COMMAND_NAME, EXECUTE_NAME
from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.validators import check_valid_options
from file_conversor.utils.typer_utils import AudioBitrateOption, AudioCodecOption, FormatOption, InputFilesArgument, OutputDirOption, VideoBitrateOption, VideoCodecOption

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES


@typer_cmd.command(
    name=EXECUTE_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Execute FFmpeg command (advanced, use with caution).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {EXECUTE_NAME} input_file.webm -od output_dir/ -f mp4 --audio-bitrate 192`

        - `file_conversor {COMMAND_NAME} {EXECUTE_NAME} input_file.mp4 -f mp3 -fa "-c:a libmp3lame -pass 1"`
    """)
def execute(
    input_files: Annotated[List[Path], InputFilesArgument(FFmpegBackend)],

    file_format: Annotated[str, FormatOption(FFmpegBackend)],

    audio_bitrate: Annotated[int, AudioBitrateOption()] = CONFIG["audio-bitrate"],

    video_bitrate: Annotated[int, VideoBitrateOption()] = CONFIG["video-bitrate"],

    audio_codec: Annotated[str | None, AudioCodecOption(FFmpegBackend.get_supported_audio_codecs())] = None,

    video_codec: Annotated[str | None, VideoCodecOption(FFmpegBackend.get_supported_video_codecs())] = None,

    audio_filters: Annotated[List[str], typer.Option("--audio-filter", "-af",
                                                     help=f'{_("Apply a custom FFmpeg audio filter")} {_("(advanced option, use with caution). Uses the same format as FFmpeg filters (e.g., filter=option1=value1:option2=value2:...). Filters are applied in the order they appear in the command.")}. {_('Defaults to None (do not apply custom filters)')}.',
                                                     )] = [],

    video_filters: Annotated[List[str], typer.Option("--video-filter", "-vf",
                                                     help=f'{_("Apply a custom FFmpeg video filter")} {_("(advanced option, use with caution). Uses the same format as FFmpeg filters (e.g., filter=option1=value1:option2=value2:...). Filters are applied in the order they appear in the command.")}. {_('Defaults to None (do not apply custom filters)')}.',
                                                     )] = [],

    ffmpeg_args: Annotated[str, typer.Option("--ffmpeg-args", "-fa",
                                             help=f'{_("Apply a custom FFmpeg output arguments (advanced option, use with caution).")}. {_('Defaults to None')}.',
                                             )] = "",

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    # init ffmpeg
    ffmpeg_backend = FFmpegBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
        overwrite_output=STATE["overwrite-output"],
    )

    # set filters
    audio_filters_obj = [FFmpegFilter.from_str(f) for f in audio_filters]
    video_filters_obj = [FFmpegFilter.from_str(f) for f in video_filters]

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        ffmpeg_backend.set_files(input_file=input_file, output_file=output_file)
        ffmpeg_backend.set_audio_codec(codec=audio_codec, bitrate=audio_bitrate, filters=audio_filters_obj)
        ffmpeg_backend.set_video_codec(codec=video_codec, bitrate=video_bitrate, filters=video_filters_obj)

        # display current progress
        ffmpeg_backend.execute(
            progress_callback=progress_mgr.update_progress,
            out_opts=shlex.split(ffmpeg_args),
        )
        progress_mgr.complete_step()

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_suffix=f".{file_format}")

    logger.info(f"{_('FFMpeg execution')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
