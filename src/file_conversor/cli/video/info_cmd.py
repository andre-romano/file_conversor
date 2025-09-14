
# src\file_conversor\cli\video\info_cmd.py

import typer

from rich import print

from typing import Annotated, List
from datetime import timedelta
from pathlib import Path

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.console import Group

# user-provided modules
from file_conversor.backend import FFprobeBackend

from file_conversor.cli.video._typer import OTHERS_PANEL as RICH_HELP_PANEL
from file_conversor.cli.video._typer import COMMAND_NAME, INFO_NAME

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils.formatters import format_bytes, format_bitrate
from file_conversor.utils.typer_utils import InputFilesArgument

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = FFprobeBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    # FFMPEG commands
    icons_folder_path = Environment.get_icons_folder()
    for ext in FFprobeBackend.SUPPORTED_IN_VIDEO_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="info",
                description="Get Info",
                command=f'cmd /k "{Environment.get_executable()} "{COMMAND_NAME}" "{INFO_NAME}" "%1""',
                icon=str(icons_folder_path / 'info.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=INFO_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Get information about a audio/video file.')}

        {_('This command retrieves metadata and other information about the audio / video file')}:

        - {_('Format')} (mp3, mp4, mov, etc)

        - {_('Duration')} (HH:MM:SS)

        - {_('Other properties')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {INFO_NAME} filename.webm`

        - `file_conversor {COMMAND_NAME} {INFO_NAME} other_filename.mp3`
    """)
def info(
    input_files: Annotated[List[Path], InputFilesArgument(FFprobeBackend)],
):

    ffprobe_backend = FFprobeBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )
    for filename in input_files:
        formatted = []
        logger.info(f"{_('Parsing file metadata for')} '{filename}' ...")
        metadata = ffprobe_backend.info(filename)
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
