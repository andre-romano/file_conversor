
# src\file_conversor\command\config\set_cmd.py

from enum import Enum
from pathlib import Path

# user-provided modules
from file_conversor.backend import (
    FFmpegBackend,
    GhostscriptBackend,
    Img2PDFBackend,
    PillowBackend,
)
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ConfigSetCommand:
    EXTERNAL_DEPENDENCIES: set[str] = set()

    class SupportedInFormats(Enum):
        """empty enum since this command doesn't take input files."""

    class SupportedOutFormats(Enum):
        """empty enum since this command doesn't take input files."""

    VideoQuality = FFmpegBackend.VideoQuality
    VideoEncoding = FFmpegBackend.VideoEncoding

    VideoOutFormat = FFmpegBackend.SupportedOutVideoFormats
    AudioOutFormat = FFmpegBackend.SupportedOutAudioFormats

    ImageFitMode = Img2PDFBackend.FitMode
    ImagePageLayout = Img2PDFBackend.PageLayout
    ImageResamplingOption = PillowBackend.ResamplingOption

    PdfCompression = GhostscriptBackend.Compression

    @classmethod
    def set(
        cls,
        cache_enabled: bool,
        cache_expire_after: int,
        language: str,
        install_deps: str | None,
        port: int,
        audio_bitrate: int | None,
        video_bitrate: int | None,
        audio_format: AudioOutFormat,
        video_format: VideoOutFormat,
        video_encoding_speed: VideoEncoding,
        video_quality: VideoQuality,
        image_quality: int,
        image_dpi: int,
        image_fit: ImageFitMode,
        image_page_size: ImagePageLayout,
        image_resampling: ImageResamplingOption,
        pdf_compression: PdfCompression,
        gui_zoom: int,
        gui_output_dir: Path,
    ):
        # update the configuration dictionary
        CONFIG.cache_enabled = cache_enabled
        CONFIG.cache_expire_after = cache_expire_after
        CONFIG.api_port = port
        CONFIG.language = language
        CONFIG.install_deps = None if install_deps == "None" or install_deps is None else bool(install_deps.capitalize())
        CONFIG.audio_bitrate = audio_bitrate
        CONFIG.video_bitrate = video_bitrate
        CONFIG.audio_format = audio_format.value
        CONFIG.video_format = video_format.value
        CONFIG.video_encoding_speed = video_encoding_speed.value
        CONFIG.video_quality = video_quality.value
        CONFIG.image_quality = image_quality
        CONFIG.image_dpi = image_dpi
        CONFIG.image_fit = image_fit.value
        CONFIG.image_page_size = image_page_size.value
        CONFIG.image_resampling = image_resampling.value
        CONFIG.pdf_compression = pdf_compression.value
        CONFIG.gui_zoom = gui_zoom
        CONFIG.gui_output_dir = str(gui_output_dir.resolve())

        Configuration.set(CONFIG)
        Configuration.save()
        logger.info(f"{_('Configuration file updated')}")


__all__ = [
    "ConfigSetCommand",
]
