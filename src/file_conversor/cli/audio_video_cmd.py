
# src\file_conversor\cli\audio_video_cmd.py

import subprocess
import time
import typer

from typing import Annotated
from datetime import timedelta
from pathlib import Path

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.console import Group

# user-provided modules
from file_conversor.backend import FFmpegBackend

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.rich import get_progress_bar
from file_conversor.utils.validators import check_positive_integer, check_file_format
from file_conversor.utils.formatters import format_bitrate, format_bytes

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

audio_video_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    # FFMPEG commands
    icons_folder_path = Environment.get_icons_folder()
    for ext in FFmpegBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="info",
                description="Get Info",
                command=f'cmd /k "{Environment.get_executable()} audio-video info "%1""',
                icon=str(icons_folder_path / 'info.ico'),
            ),
            WinContextCommand(
                name="to_avi",
                description="To AVI",
                command=f'{Environment.get_executable()} audio-video convert "%1" -o "%1.avi"',
                icon=str(icons_folder_path / 'avi.ico'),
            ),
            WinContextCommand(
                name="to_mp4",
                description="To MP4",
                command=f'{Environment.get_executable()} audio-video convert "%1" -o "%1.mp4"',
                icon=str(icons_folder_path / 'mp4.ico'),
            ),
            WinContextCommand(
                name="to_mkv",
                description="To MKV",
                command=f'{Environment.get_executable()} audio-video convert "%1" -o "%1.mkv"',
                icon=str(icons_folder_path / 'mkv.ico'),
            ),
            WinContextCommand(
                name="to_mp3",
                description="To MP3",
                command=f'{Environment.get_executable()} audio-video convert "%1" -o "%1.mp3"',
                icon=str(icons_folder_path / 'mp3.ico'),
            ),
            WinContextCommand(
                name="to_m4a",
                description="To M4A",
                command=f'{Environment.get_executable()} audio-video convert "%1" -o "%1.m4a"',
                icon=str(icons_folder_path / 'm4a.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


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

        - `file_conversor audio-video info filename.webm`

        - `file_conversor audio-video info other_filename.mp3`
    """)
def info(
    filename: Annotated[str, typer.Argument(
        help=f"{_('File')} ({', '.join(FFmpegBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, FFmpegBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],
):

    formatted = []
    metadata: dict
    with get_progress_bar() as progress:
        ffprobe_task = progress.add_task(f"{_('Parsing file metadata')} ...", total=None)

        ffmpeg_backend = FFmpegBackend(
            install_deps=CONFIG['install-deps'],
            verbose=STATE["verbose"],
        )
        metadata = ffmpeg_backend.get_file_info(filename)
        progress.update(ffprobe_task, total=100, completed=100)

    # 📁 General file information
    if "format" in metadata:
        format_info: dict = metadata["format"]

        duration = format_info.get('duration', 'N/A')
        if duration != "N/A":
            duration_secs = int(float(duration))
            duration_td = timedelta(seconds=duration_secs)
            duration = str(duration_td)
        size = format_info.get("size", "N/A")
        if size != "N/A":
            size = format_bytes(float(size))
        bitrate = format_info.get('bit_rate', 'N/A')
        if bitrate != "N/A":
            bitrate = format_bitrate(int(bitrate))

        formatted.append(Text(f"📁 {_('File Information')}:", style="bold cyan"))
        formatted.append(f"  - {_('Name')}: {filename}")
        formatted.append(f"  - {_('Format')}: {format_info.get('format_name', 'N/A')}")
        formatted.append(f"  - {_('Duration')}: {duration}")
        formatted.append(f"  - {_('Size')}: {size}")
        formatted.append(f"  - {_('Bitrate')}: {bitrate}")

    # 🎬 Streams de Mídia
    if "streams" in metadata:
        if len(metadata["streams"]) > 0:
            formatted.append(Text(f"\n🎬 {_("Media Streams")}:", style="bold yellow"))
        for i, stream in enumerate(metadata["streams"]):
            stream_type = stream.get("codec_type", "unknown")
            codec = stream.get("codec_name", "N/A")
            resolution = f"{stream.get('width', '?')}x{stream.get('height', '?')}" if stream_type == "video" else ""
            bitrate = stream.get("bit_rate", "N/A")

            if bitrate != "N/A":
                bitrate = format_bitrate(int(bitrate))

            formatted.append(f"\n  🔹 {_('Stream')} #{i} ({stream_type.upper()}):")
            formatted.append(f"    - {_('Codec')}: {codec}")
            if resolution:
                formatted.append(f"    - {_('Resolution')}: {resolution}")
            formatted.append(f"    - {_('Bitrate')}: {bitrate}")
            if stream_type == "audio":
                formatted.append(f"    - {_('Sampling rate')}: {stream.get('sample_rate', 'N/A')} Hz")
                formatted.append(f"    - {_('Channels')}: {stream.get('channels', 'N/A')}")

    # 📖 Capítulos
    if "chapters" in metadata:
        if len(metadata["chapters"]) > 0:
            formatted.append(Text(f"\n📖 {_('Chapters')}:", style="bold green"))
        for chapter in metadata["chapters"]:
            title = chapter.get('tags', {}).get('title', 'N/A')
            start = chapter.get('start_time', 'N/A')
            formatted.append(f"  - {title} ({_('Time')}: {start}s)")

    # Agrupar e exibir tudo com Rich
    group = Group(*formatted)
    print(Panel(group, title=f"🧾 {_('File Analysis')}", border_style="blue"))


# audio_video convert
@audio_video_cmd.command(
    help=f"""
        {_('Convert a audio/video file to a different format.')}

        {_('This command can be used to convert audio or video files to the specified format.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor audio-video convert input_file.webm -o output_file.mp4 --audio-bitrate 192`

        - `file_conversor audio-video convert input_file.mp4 -o output_file.mp3`
    """)
def convert(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file')} ({', '.join(FFmpegBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, FFmpegBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],
    output_file: Annotated[str, typer.Option("--output", "-o",
                                             help=f"{_('Output file')} ({', '.join(FFmpegBackend.SUPPORTED_OUT_FORMATS)})",
                                             callback=lambda x: check_file_format(x, FFmpegBackend.SUPPORTED_OUT_FORMATS),
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

    out_ext = Path(output_file).suffix[1:]

    # configure out options
    out_options.extend(["-b:a", f"{audio_bitrate}k"])
    if out_ext in FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS:
        out_options.extend(["-b:v", f"{video_bitrate}k"])

    # execute ffmpeg
    ffmpeg_backend = FFmpegBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )
    input_file_duration = ffmpeg_backend.calculate_file_total_duration(input_file)
    process = ffmpeg_backend.convert(
        input_file,
        output_file,
        in_options=in_options,
        out_options=out_options,
    )

    # display current progress
    with get_progress_bar() as progress:
        ffmpeg_task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=100)
        while process.poll() is None:
            ffmpeg_completed = FFmpegBackend.get_convert_progress(process, input_file_duration)
            progress.update(ffmpeg_task, completed=ffmpeg_completed)
            time.sleep(0.25)
        progress.update(ffmpeg_task, completed=100)

    process.wait()
    if process.returncode != 0:
        raise RuntimeError(process.stdout)

    logger.info(f"{_('FFMpeg convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green] ({process.returncode})")
