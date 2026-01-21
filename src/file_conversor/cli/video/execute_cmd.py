
# src\file_conversor\cli\video\execute_cmd.py

import shlex
import typer

from typing import Annotated, Iterable, List
from pathlib import Path

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import AudioBitrateOption, AudioCodecOption, FormatOption, InputFilesArgument, OutputDirOption, VideoBitrateOption, VideoCodecOption

from file_conversor.backend import FFmpegBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation
from file_conversor.system.win.ctx_menu import WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoExecuteTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # no context menu for this command

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.execute,
            help=f"""
        {_('Execute FFmpeg command (advanced, use with caution).')}
    """,
            epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {group_name} {command_name} input_file.webm -od output_dir/ -f mp4 --audio-bitrate 192`

        - `file_conversor {group_name} {command_name} input_file.mp4 -f mp3 -fa "-c:a libmp3lame -pass 1"`
    """)

    def execute(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(FFmpegBackend)],
        file_format: Annotated[str, FormatOption(FFmpegBackend)],

        audio_bitrate: Annotated[int, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int, VideoBitrateOption()] = CONFIG.video_bitrate,

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
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
            overwrite_output=STATE.overwrite_output.enabled,
        )

        # set filters
        audio_filters_obj = [FFmpegBackend.build_filter(f) for f in audio_filters]
        video_filters_obj = [FFmpegBackend.build_filter(f) for f in video_filters]

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            ffmpeg_backend.set_files(input_file=input_file, output_file=output_file)
            ffmpeg_backend.set_audio_codec(codec=audio_codec, bitrate=audio_bitrate, filters=audio_filters_obj)
            ffmpeg_backend.set_video_codec(codec=video_codec, bitrate=video_bitrate, filters=video_filters_obj)

            # display current progress
            ffmpeg_backend.execute(
                progress_callback=progress_mgr.update_progress,
                out_opts=shlex.split(ffmpeg_args),
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_suffix=f".{file_format}")

        logger.info(f"{_('FFMpeg execution')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "VideoExecuteTyperCommand",
]
