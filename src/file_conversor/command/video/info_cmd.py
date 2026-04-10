
# src\file_conversor\command\video\info_cmd.py

from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any, Callable, override

from file_conversor.backend.audio_video import FFprobeBackend
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import CONFIG, LOG, STATE, get_translation
from file_conversor.utils.formatters import format_bitrate, format_bytes


_ = get_translation()
logger = LOG.getLogger(__name__)


VideoInfoExternalDependencies = FFprobeBackend.EXTERNAL_DEPENDENCIES
VideoInfoInFormats = FFprobeBackend.SupportedInFormats
VideoInfoOutFormats = FFprobeBackend.SupportedOutFormats


@dataclass
class VideoInfoFormat:
    filename: Path
    file_format: str
    duration: str
    size: str
    bitrate: str

    @classmethod
    def get(cls, filename: Path, metadata: dict[str, Any]):
        format_info = metadata.get("format", {})

        duration = str(format_info.get('duration', 'N/A'))
        if duration != "N/A":
            duration_secs = int(float(duration))
            duration_td = timedelta(seconds=duration_secs)
            duration = str(duration_td)

        size = str(format_info.get("size", "N/A"))
        if size != "N/A":
            size = format_bytes(float(size))

        bitrate = str(format_info.get('bit_rate', 'N/A'))
        if bitrate != "N/A":
            bitrate = format_bitrate(int(bitrate))

        file_format = str(format_info.get('format_name', 'N/A'))
        return VideoInfoFormat(
            filename=filename,
            file_format=file_format,
            duration=duration,
            size=size,
            bitrate=bitrate,
        )


@dataclass
class VideoInfoStream:
    type: str
    codec: str
    bitrate: str
    resolution: str
    sample_rate: str
    channels: str

    @classmethod
    def get(cls, stream: dict[str, Any]):
        codec = stream.get("codec_name", "N/A")
        bitrate = stream.get("bit_rate", "N/A")

        if bitrate != "N/A":
            bitrate = format_bitrate(int(bitrate))

        stream_type = str(stream.get("codec_type", "unknown")).upper()
        resolution = f"{stream.get('width', '?')}x{stream.get('height', '?')}" if stream_type == "VIDEO" else ""
        sample_rate = f"{stream.get('sample_rate', '?')} Hz" if stream_type == "AUDIO" else ""
        channels = str(stream.get('channels', '?')) if stream_type == "AUDIO" else ""

        return VideoInfoStream(
            type=stream_type,
            codec=codec,
            bitrate=bitrate,
            resolution=resolution,
            sample_rate=sample_rate,
            channels=channels,
        )


@dataclass
class VideoInfoChapter:
    title: str
    start_time: str

    @classmethod
    def get(cls, chapter: dict[str, Any]):
        title = chapter.get('tags', {}).get('title', 'N/A')
        start_sec = int(chapter.get('start_time', 0))
        start_td = timedelta(seconds=start_sec)
        start_time = str(start_td)
        return VideoInfoChapter(
            title=title,
            start_time=start_time,
        )


@dataclass
class VideoInfoDataModel:
    filename: Path
    format_info: VideoInfoFormat
    streams: list[VideoInfoStream]
    chapters: list[VideoInfoChapter]


@dataclass
class VideoInfoMarkdownStrategy:
    output: list[VideoInfoDataModel]

    def _get_stream_info(self, streams: list[VideoInfoStream]) -> list[str]:
        output_text: list[str] = []
        for idx, stream in enumerate(streams):
            output_text.extend([
                f"- {_('Stream')} #{idx} ({stream.type}):",
                f"  - {_('Codec')}: {stream.codec}",
                f"  - {_('Bitrate')}: {stream.bitrate}",
                f"  - {_('Resolution')}: {stream.resolution}" if stream.resolution else "",
                f"  - {_('Sampling rate')}: {stream.sample_rate}" if stream.sample_rate else "",
                f"  - {_('Channels')}: {stream.channels}" if stream.channels else "",
            ])
        return output_text

    def _get_chapters_info(self, chapters: list[VideoInfoChapter]) -> list[str]:
        output_text: list[str] = []
        for chapter in chapters:
            output_text.extend([
                f"- {chapter.title} ({_('Time')}: {chapter.start_time})",
            ])
        return output_text

    def get_output_markdown(self) -> str:
        markdown_str = ""
        for data in self.output:
            markdown_str += "\n".join([
                f"## {_('File Information')}:",
                f"- {_('Name')}: {data.filename.name}",
                f"- {_('Format')}: {data.format_info.file_format}",
                f"- {_('Duration')}: {data.format_info.duration}",
                f"- {_('Size')}: {data.format_info.size}",
                f"- {_('Bitrate')}: {data.format_info.bitrate}",
                f"\n",
                f"### {_("Media Streams")}:",
                *self._get_stream_info(data.streams),
                f"\n",
                f"### {_('Chapters')}:",
                *self._get_chapters_info(data.chapters),
            ])
            markdown_str += f"\n---\n"
        return markdown_str


class VideoInfoCommand(AbstractCommand[VideoInfoInFormats, VideoInfoOutFormats]):
    input_files: list[Path]
    output: list[VideoInfoDataModel] = []

    @classmethod
    @override
    def _external_dependencies(cls):
        return VideoInfoExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return VideoInfoInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return VideoInfoOutFormats

    @override
    def execute(self):
        backend = FFprobeBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=Path(),
            out_stem="_",
            overwrite_output=STATE.overwrite_output.enabled,
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Getting info for file')} '{data.input_file}' ...")
            # display current progress
            try:
                metadata = backend.info(data.input_file)
                self.output.append(
                    VideoInfoDataModel(
                        filename=data.input_file,
                        format_info=VideoInfoFormat.get(data.input_file, metadata),
                        streams=[
                            VideoInfoStream.get(stream)
                            for stream in metadata.get("streams", [])
                        ],
                        chapters=[
                            VideoInfoChapter.get(chapter)
                            for chapter in metadata.get("chapters", [])
                        ],
                    )
                )
            except Exception as e:
                logger.error(f"{_('Error getting info for file')} '{data.input_file}': {e}")
            self.progress_callback(get_progress(100.0))

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File info retrieval')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "VideoInfoExternalDependencies",
    "VideoInfoInFormats",
    "VideoInfoOutFormats",
    "VideoInfoFormat",
    "VideoInfoStream",
    "VideoInfoChapter",
    "VideoInfoDataModel",
    "VideoInfoMarkdownStrategy",
    "VideoInfoCommand",
]
