# src/file_conversor/utils/backend/ffprobe_utils.py

import subprocess

from datetime import timedelta
from pathlib import Path

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.console import Group

# user-provided imports
from file_conversor.backend.audio_video import FFprobeBackend

from file_conversor.utils.dominate_utils import br, div
from file_conversor.utils.formatters import format_bitrate, format_bytes

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


class _FFprobeFormatInfo:
    def __init__(self, input_file: Path, metadata: dict) -> None:
        super().__init__()
        self.input_file = input_file
        self.format_info = metadata.get("format", {})

    def _parse(self):
        duration = self.format_info.get('duration', 'N/A')
        if duration != "N/A":
            duration_secs = int(float(duration))
            duration_td = timedelta(seconds=duration_secs)
            duration = str(duration_td)

        size = self.format_info.get("size", "N/A")
        if size != "N/A":
            size = format_bytes(float(size))

        bitrate = self.format_info.get('bit_rate', 'N/A')
        if bitrate != "N/A":
            bitrate = format_bitrate(int(bitrate))

        format_name = self.format_info.get('format_name', 'N/A')
        return duration, size, bitrate, format_name

    def rich(self):
        duration, size, bitrate, format_name = self._parse()
        return [
            Text(f"📁 {_('File Information')}:", style="bold cyan"),
            f"  - {_('Name')}: {self.input_file.name}",
            f"  - {_('Format')}: {format_name}",
            f"  - {_('Duration')}: {duration}",
            f"  - {_('Size')}: {size}",
            f"  - {_('Bitrate')}: {bitrate}",
        ]

    def div(self):
        duration, size, bitrate, format_name = self._parse()
        with div() as result:
            div(f"{_('File Information')}:")
            div(f"  - {_('Name')}: {self.input_file.name}")
            div(f"  - {_('Format')}: {format_name}")
            div(f"  - {_('Duration')}: {duration}")
            div(f"  - {_('Size')}: {size}")
            div(f"  - {_('Bitrate')}: {bitrate}")
            br()
        return result


class _FFprobeStreamsInfo:
    def __init__(self, input_file: Path, metadata: dict) -> None:
        super().__init__()
        self.input_file = input_file
        self.streams_info = metadata.get("streams", [])

    def _parse(self, stream: dict):
        stream_type = str(stream.get("codec_type", "unknown")).upper()
        codec = stream.get("codec_name", "N/A")
        resolution = f"{stream.get('width', '?')}x{stream.get('height', '?')}" if stream_type == "video" else ""
        bitrate = stream.get("bit_rate", "N/A")

        if bitrate != "N/A":
            bitrate = format_bitrate(int(bitrate))

        sample_rate = f"{stream.get('sample_rate', 'N/A')} Hz" if stream_type == "AUDIO" else ""
        channels = stream.get('channels', 'N/A') if stream_type == "AUDIO" else ""
        return stream_type, codec, resolution, bitrate, sample_rate, channels

    def rich(self):
        formatted = []
        if self.streams_info:
            formatted.append(Text(f"\n🎬 {_("Media Streams")}:", style="bold yellow"))
        for i, stream in enumerate(self.streams_info):
            stream_type, codec, resolution, bitrate, sample_rate, channels = self._parse(stream)

            formatted.append(f"\n  🔹 {_('Stream')} #{i} ({stream_type}):")
            formatted.append(f"    - {_('Codec')}: {codec}")
            if resolution:
                formatted.append(f"    - {_('Resolution')}: {resolution}")
            formatted.append(f"    - {_('Bitrate')}: {bitrate}")
            if stream_type == "audio":
                formatted.append(f"    - {_('Sampling rate')}: {sample_rate} Hz")
                formatted.append(f"    - {_('Channels')}: {channels}")
        return formatted

    def div(self):
        with div() as result:
            if self.streams_info:
                div(f"{_("Media Streams")}:")
            for i, stream in enumerate(self.streams_info):
                stream_type, codec, resolution, bitrate, sample_rate, channels = self._parse(stream)

                div(f"    {_('Stream')} #{i} ({stream_type.upper()}):")
                div(f"    - {_('Codec')}: {codec}")
                if resolution:
                    div(f"    - {_('Resolution')}: {resolution}")
                div(f"    - {_('Bitrate')}: {bitrate}")
                if stream_type == "audio":
                    div(f"    - {_('Sampling rate')}: {sample_rate}")
                    div(f"    - {_('Channels')}: {channels}")
                br()
            br()
        return result


class _FFprobeChaptersInfo:
    def __init__(self, input_file: Path, metadata: dict) -> None:
        super().__init__()
        self.input_file = input_file
        self.chapters_info = metadata.get("chapters", [])

    def _parse(self, chapter: dict):
        title = chapter.get('tags', {}).get('title', 'N/A')
        start = f"{chapter.get('start_time', 'N/A')}s"
        return title, start

    def rich(self):
        formatted = []
        if self.chapters_info:
            formatted.append(Text(f"\n📖 {_('Chapters')}:", style="bold green"))
        for chapter in self.chapters_info:
            title, start = self._parse(chapter)
            formatted.append(f"  - {title} ({_('Time')}: {start})")
        return formatted

    def div(self):
        with div() as result:
            if self.chapters_info:
                div(f"{_('Chapters')}:")
            for chapter in self.chapters_info:
                title, start = self._parse(chapter)
                div(f"  - {title} ({_('Time')}: {start})")
        return result


class FFprobeParser:
    def __init__(self, backend: FFprobeBackend, input_file: Path) -> None:
        super().__init__()
        self.input_file = input_file
        self.backend = backend

    def run(self):
        try:
            self.metadata = self.backend.info(self.input_file)
        except subprocess.CalledProcessError:
            raise RuntimeError(f"{_('File')} '{self.input_file}' {_('is corrupted or has inconsistencies')}")

    def get_format(self):
        return _FFprobeFormatInfo(self.input_file, self.metadata)

    def get_streams(self):
        return _FFprobeStreamsInfo(self.input_file, self.metadata)

    def get_chapters(self):
        return _FFprobeChaptersInfo(self.input_file, self.metadata)


__all__ = [
    "FFprobeParser",
]
