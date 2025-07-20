
# src\cli\audio_video_cmd.py

import subprocess
import time
import typer

from typing import Annotated, Optional

from rich import print
from rich.pretty import Pretty
from rich.progress import Progress

# user-provided modules
from backend import FFmpegBackend

from config import get_translation
from config import Configuration, State

from utils import check_positive_integer, check_format
from utils import File

# get app config
_ = get_translation()
CONFIG = Configuration.get_instance()
STATE = State.get_instance()

audio_video_cmd = typer.Typer()


# audio_video info
@audio_video_cmd.command(
    help=f"""
        {_('Get information about a audio/video file.')}

        {_('This command retrieves metadata and other information about the audio / video file')}:

        - {_('Format')} (mp3, mp4, mov, etc)

        - {_('Duration')} (HH:MM:SS)

        - Bitrate

        - {_('Other properties')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor audio_video info filename.webm`

        - `file_conversor audio_video info other_filename.mp3`
    """)
def info(
    filename: Annotated[str, typer.Argument(
        help=_("File path"),
        callback=lambda x: x if check_format(
            File(x).get_extension(), FFmpegBackend.SUPPORTED_IN_FORMATS
        ) else x,
    )],
):
    pass


# audio_video convert
@audio_video_cmd.command(
    help=f"""
        {_('Convert a audio/video file to a different format.')}

        {_('This command can be used to convert audio or video files to the specified format.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor audio_video convert input_file.webm output_file.mp4 --audio-bitrate 192`

        - `file_conversor audio_video convert input_file.mp4 output_file.mp3`
    """)
def convert(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file path')} ({', '.join(FFmpegBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: x if check_format(
            File(x).get_extension(), FFmpegBackend.SUPPORTED_IN_FORMATS
        ) else x,
    )],
    output_file: Annotated[str, typer.Argument(
        help=f"{_('Output file path')} ({', '.join(FFmpegBackend.SUPPORTED_OUT_FORMATS)})",
        callback=lambda x: x if check_format(
            File(x).get_extension(), FFmpegBackend.SUPPORTED_OUT_FORMATS
        ) else x,
    )],
    audio_bitrate: Annotated[int, typer.Option("--audio-bitrate", "-ab",
                                               help=_("Audio bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["audio-bitrate"],

    video_bitrate: Annotated[int, typer.Option("--video-bitrate", "-vb",
                                               help=_("Video bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["video-bitrate"],
):
    process: subprocess.Popen | None = None
    in_options = []
    out_options = []

    # configure out options
    out_options.extend(["-b:a", f"{audio_bitrate}k"])
    if File(output_file).get_extension() in FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS:
        out_options.extend(["-b:v", f"{video_bitrate}k"])

    # execute ffmpeg
    ffmpeg_backend = FFmpegBackend(
        input_file,
        output_file,
        verbose=STATE["verbose"],
        in_options=in_options,
        out_options=out_options,
    )
    process = ffmpeg_backend.execute()

    # display current progress
    with Progress() as progress:
        ffmpeg_task = progress.add_task(
            f"[blue]{_('Processing file')}...", total=100)
        while process.poll() is None:
            progress.update(
                ffmpeg_task, completed=ffmpeg_backend.get_progress())
            time.sleep(0.25)

    process.wait()
    progress.update(ffmpeg_task, completed=100)

    if process.returncode == 0:
        print(f"--------------------------------")
        print(
            f"{_('FFMpeg convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green] ({process.returncode})")
        print(f"--------------------------------")
    else:
        # print output
        if process.stderr:
            for line in process.stderr:
                print(line)
        if process.stdout:
            for line in process.stdout:
                print(line)
        print(f"\n--------------------------------")
        print(
            f"{_('FFMpeg convertion')}: [red][bold]{_('FAILED')}[/bold][/red] ({process.returncode if process else "?"})")
        print(f"--------------------------------")
