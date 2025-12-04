
# src\file_conversor\cli\video\_ffmpeg_cmd.py

from rich import print

from typing import Annotated, Any, Callable, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend
from file_conversor.backend.audio_video.ffmpeg_filter import FFmpegFilter

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES


def ffmpeg_audio_run(  # pyright: ignore[reportUnusedFunction]
    input_files: List[Path],

    file_format: str,
    out_stem: str = "",

    audio_bitrate: int = 0,
    audio_codec: str | None = None,

    output_dir: Path = Path(),
    progress_callback: Callable[[float, ProgressManager], Any] | None = None,
):
    # init ffmpeg
    ffmpeg_backend = FFmpegBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
        overwrite_output=STATE["overwrite-output"],
    )

    # set filters
    audio_filters: list[FFmpegFilter] = []

    two_pass = (audio_bitrate > 0)

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        ffmpeg_backend.set_files(input_file=input_file, output_file=output_file)
        ffmpeg_backend.set_audio_codec(codec=audio_codec, bitrate=audio_bitrate, filters=audio_filters)

        progress_update_cb = progress_mgr.update_progress
        if progress_callback is not None:
            def progress_update_cb(step_progress: float): return progress_callback(step_progress, progress_mgr)  # pyright: ignore[reportOptionalCall]

        progress_complete_cb = progress_mgr.complete_step
        if progress_callback is not None:
            def progress_complete_cb(): return progress_callback(progress_mgr.complete_step(), progress_mgr)  # pyright: ignore[reportOptionalCall]

        # display current progress
        ffmpeg_backend.execute(
            progress_callback=progress_update_cb,
            pass_num=1 if two_pass else 0,
        )
        progress_complete_cb()

        if two_pass:
            # display current progress
            ffmpeg_backend.execute(
                progress_callback=progress_update_cb,
                pass_num=2,
            )
            progress_complete_cb()

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, steps=2 if two_pass else 1, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_suffix=f".{file_format}", out_stem=out_stem)

    logger.info(f"{_('FFMpeg result')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "ffmpeg_audio_run",
]
