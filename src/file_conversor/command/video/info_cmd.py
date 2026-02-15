
# src\file_conversor\command\video\info_cmd.py

from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any, Callable, Iterable

from file_conversor.backend.audio_video import FFprobeBackend
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.utils.formatters import format_bitrate, format_bytes


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoInfoCommand:
    EXTERNAL_DEPENDENCIES = FFprobeBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = FFprobeBackend.SupportedInFormats

    @dataclass
    class FormatInfo:
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
            return VideoInfoCommand.FormatInfo(
                filename=filename,
                file_format=file_format,
                duration=duration,
                size=size,
                bitrate=bitrate,
            )

    @dataclass
    class StreamInfo:
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

            return VideoInfoCommand.StreamInfo(
                type=stream_type,
                codec=codec,
                bitrate=bitrate,
                resolution=resolution,
                sample_rate=sample_rate,
                channels=channels,
            )

    @dataclass
    class ChapterInfo:
        title: str
        start_time: str

        @classmethod
        def get(cls, chapter: dict[str, Any]):
            title = chapter.get('tags', {}).get('title', 'N/A')
            start_sec = int(chapter.get('start_time', 0))
            start_td = timedelta(seconds=start_sec)
            start_time = str(start_td)
            return VideoInfoCommand.ChapterInfo(
                title=title,
                start_time=start_time,
            )

    @dataclass
    class InfoDataModel:
        filename: Path
        format_info: "VideoInfoCommand.FormatInfo"
        streams: list["VideoInfoCommand.StreamInfo"]
        chapters: list["VideoInfoCommand.ChapterInfo"]

    @classmethod
    def info(
        cls,
        input_files: list[Path],
        progress_callback: Callable[[float], Any] = lambda p: p,
    ) -> Iterable[InfoDataModel]:

        backend = FFprobeBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=Path(),
            out_stem="_",
            overwrite_output=STATE.overwrite_output.enabled,
        )

        info_list: list[VideoInfoCommand.InfoDataModel] = []

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"{_('Getting info for file')} '{data.input_file}' ...")
            # display current progress
            try:
                metadata = backend.info(data.input_file)
                info_list.append(
                    VideoInfoCommand.InfoDataModel(
                        filename=data.input_file,
                        format_info=VideoInfoCommand.FormatInfo.get(data.input_file, metadata),
                        streams=[
                            VideoInfoCommand.StreamInfo.get(stream)
                            for stream in metadata.get("streams", [])
                        ],
                        chapters=[
                            VideoInfoCommand.ChapterInfo.get(chapter)
                            for chapter in metadata.get("chapters", [])
                        ],
                    )
                )
            except Exception as e:
                logger.error(f"{_('Error getting info for file')} '{data.input_file}': {e}")
            progress_callback(get_progress(100.0))

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File info retrieval')}: [bold green]{_('SUCCESS')}[/].")
        return info_list


__all__ = [
    "VideoInfoCommand",
]
