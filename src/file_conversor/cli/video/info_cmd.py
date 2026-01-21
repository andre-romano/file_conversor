
# src\file_conversor\cli\video\info_cmd.py

from datetime import timedelta
from pathlib import Path
from typing import Annotated, Iterable, List

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.console import Group

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import InputFilesArgument

from file_conversor.backend import FFprobeBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win import WinContextCommand, WinContextMenu

from file_conversor.utils.formatters import format_bitrate, format_bytes

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoInfoTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = FFprobeBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # FFMPEG commands
        icons_folder_path = Environment.get_icons_folder()
        for ext in FFprobeBackend.SUPPORTED_IN_VIDEO_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="info",
                    description="Get Info",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / 'info.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.info,
            help=f"""
    {_('Get information about a video file.')}

    {_('This command retrieves metadata and other information about the video file')}:

    - {_('Format')} (avi, mp4, mov, etc)

    - {_('Duration')} (HH:MM:SS)

    - {_('Other properties')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} filename.webm`

    - `file_conversor {group_name} {command_name} other_filename.mp4`
""")

    def info(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(FFprobeBackend)],
    ):
        ffprobe_backend = FFprobeBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )
        for filename in input_files:
            logger.info(f"{_('Parsing file metadata for')} '{filename}' ...")
            try:
                metadata = ffprobe_backend.info(filename)

                # Agrupar e exibir tudo com Rich
                group = Group(
                    *self._get_format_info(filename, metadata),
                    *self._get_streams_info(metadata),
                    *self._get_chapters_info(metadata),
                )
                print(Panel(group, title=f"🧾 {_('File Analysis')}", border_style="blue"))
            except Exception as e:
                logger.error(f"{_('Error parsing file')} '{filename}': {e}")
                continue

    def _get_format_info(self, filename: Path, metadata: dict):
        formatted: list[str | Text] = []
        format_info = metadata.get("format", {})

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

        format_name = format_info.get('format_name', 'N/A')

        formatted = [
            Text(f"📁 {_('File Information')}:", style="bold cyan"),
            f"  - {_('Name')}: {filename.name}",
            f"  - {_('Format')}: {format_name}",
            f"  - {_('Duration')}: {duration}",
            f"  - {_('Size')}: {size}",
            f"  - {_('Bitrate')}: {bitrate}",
        ]
        return formatted

    def _get_streams_info(self, metadata: dict):
        formatted: list[str | Text] = []
        streams_info = metadata.get("streams", [])

        if streams_info:
            formatted.append(Text(f"\n🎬 {_("Media Streams")}:", style="bold yellow"))
        for i, stream in enumerate(streams_info):
            stream_type = str(stream.get("codec_type", "unknown")).upper()
            codec = stream.get("codec_name", "N/A")
            resolution = f"{stream.get('width', '?')}x{stream.get('height', '?')}" if stream_type == "video" else ""
            bitrate = stream.get("bit_rate", "N/A")

            if bitrate != "N/A":
                bitrate = format_bitrate(int(bitrate))

            sample_rate = f"{stream.get('sample_rate', 'N/A')} Hz" if stream_type == "AUDIO" else ""
            channels = stream.get('channels', 'N/A') if stream_type == "AUDIO" else ""

            formatted.append(f"\n  🔹 {_('Stream')} #{i} ({stream_type}):")
            formatted.append(f"    - {_('Codec')}: {codec}")
            if resolution:
                formatted.append(f"    - {_('Resolution')}: {resolution}")
            formatted.append(f"    - {_('Bitrate')}: {bitrate}")
            if stream_type == "audio":
                formatted.append(f"    - {_('Sampling rate')}: {sample_rate} Hz")
                formatted.append(f"    - {_('Channels')}: {channels}")
        return formatted

    def _get_chapters_info(self, metadata: dict):
        formatted: list[str | Text] = []
        chapters_info = metadata.get("chapters", [])

        if chapters_info:
            formatted.append(Text(f"\n📖 {_('Chapters')}:", style="bold green"))
        for chapter in chapters_info:
            title = chapter.get('tags', {}).get('title', 'N/A')
            start = f"{chapter.get('start_time', 'N/A')}s"
            formatted.append(f"  - {title} ({_('Time')}: {start})")
        return formatted


__all__ = [
    "VideoInfoTyperCommand",
]
