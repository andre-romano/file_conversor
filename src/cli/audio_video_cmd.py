
# src\cli\audio_video_cmd.py

import subprocess
import time
import typer

from typing import Annotated, Optional
from datetime import timedelta

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.console import Group
from rich.markdown import Markdown
from rich.pretty import Pretty
from rich.progress import Progress

# user-provided modules
from backend import FFmpegBackend

from config import get_translation
from config import Configuration, State

from utils import check_positive_integer, check_format, format_bitrate, format_bytes
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

    formatted = []
    metadata = FFmpegBackend.get_file_info(filename)
    # 📁 Informações gerais do arquivo
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

        formatted.append(Text("📁 Informações do Arquivo:", style="bold cyan"))
        formatted.append(f"  - Nome: {filename}")
        formatted.append(
            f"  - Formato: {format_info.get('format_name', 'N/A')}")
        formatted.append(f"  - Duração: {duration}")
        formatted.append(
            f"  - Tamanho: {size}")
        formatted.append(
            f"  - Bitrate: {bitrate}")

    # 🎬 Streams de Mídia
    if "streams" in metadata:
        if len(metadata["streams"]) > 0:
            formatted.append(
                Text("\n🎬 Streams de Mídia:", style="bold yellow"))
        for i, stream in enumerate(metadata["streams"]):
            stream_type = stream.get("codec_type", "unknown")
            codec = stream.get("codec_name", "N/A")
            resolution = f"{stream.get('width', '?')}x{stream.get('height', '?')}" if stream_type == "video" else ""
            bitrate = stream.get("bit_rate", "N/A")

            if bitrate != "N/A":
                bitrate = format_bitrate(int(bitrate))

            formatted.append(f"\n  🔹 Stream #{i} ({stream_type.upper()}):")
            formatted.append(f"    - Codec: {codec}")
            if resolution:
                formatted.append(f"    - Resolução: {resolution}")
            formatted.append(f"    - Bitrate: {bitrate}")
            if stream_type == "audio":
                formatted.append(
                    f"    - Taxa de amostragem: {stream.get('sample_rate', 'N/A')} Hz")
                formatted.append(
                    f"    - Canais: {stream.get('channels', 'N/A')}")

    # 📖 Capítulos
    if "chapters" in metadata:
        if len(metadata["chapters"]) > 0:
            formatted.append(Text("\n📖 Capítulos:", style="bold green"))
        for chapter in metadata["chapters"]:
            title = chapter.get('tags', {}).get('title', 'N/A')
            start = chapter.get('start_time', 'N/A')
            formatted.append(f"  - {title} (Tempo: {start}s)")

    # Agrupar e exibir tudo com Rich
    group = Group(*formatted)
    print(
        Panel(group, title=f"🧾 Análise do Arquivo", border_style="blue"))


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
