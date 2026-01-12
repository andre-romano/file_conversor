
# src\file_conversor\cli\config\set_cmd.py

from pathlib import Path
import typer

from typing import Annotated

from rich import print

# user-provided modules
import file_conversor.cli.config.show_cmd as show_cmd

from file_conversor.cli.config._typer import COMMAND_NAME, SET_NAME

from file_conversor.backend import Img2PDFBackend, PillowBackend, FFmpegBackend, GhostscriptBackend
from file_conversor.config import Configuration, Log, locale, get_translation, AVAILABLE_LANGUAGES

from file_conversor.utils.typer_utils import VideoEncodingSpeedOption, VideoQualityOption
from file_conversor.utils.validators import check_dir_exists, check_is_bool_or_none, check_positive_integer, check_valid_options

# app configuration
CONFIG = Configuration.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# create command
typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = set()


@typer_cmd.command(
    name=SET_NAME,
    help=f"""
        {_('Configure the default options for the app.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor configure --video-bitrate 5000`

        - `file_conversor configure --audio-bitrate 128`
    """,
)
def set(
    cache_enabled: Annotated[bool, typer.Option("--cache-enabled", "-ce",
                                                help=_("Enable or disable HTTP cache."),
                                                callback=check_is_bool_or_none,
                                                is_flag=True,
                                                )] = CONFIG.cache_enabled,


    cache_expire_after: Annotated[int, typer.Option("--cache-expire-after", "-cea",
                                                    help=_("Set HTTP cache expiration time in seconds."),
                                                    min=1,
                                                    )] = CONFIG.cache_expire_after,

    language: Annotated[str, typer.Option("--language", "-l",
                                          help=f'{_("Set preferred language for app (if available). Available languages:")} {", ".join(sorted(AVAILABLE_LANGUAGES))}. {_("Defaults to system preffered language or 'en_US' (English - United States)")}.',
                                          callback=lambda x: check_valid_options(x, AVAILABLE_LANGUAGES),
                                          )] = locale.normalize_lang_code(CONFIG.language) or locale.get_default_language(),

    install_deps: Annotated[str | None, typer.Option("--install-deps", "-install",
                                                     help=_("Install missing external dependencies action. 'True' for auto install. 'False' to not install missing dependencies. 'None' to ask user for action."),
                                                     callback=check_is_bool_or_none,
                                                     )] = str(CONFIG.install_deps),

    port: Annotated[int, typer.Option("--port", "-p",
                                      help=f'{_("Set preferred listen port for app (if available). Ports below 1024 require root privileges. Defaults to 5000.")}.',
                                      min=1, max=65535,
                                      )] = CONFIG.port,

    audio_bitrate: Annotated[int, typer.Option("--audio-bitrate", "-ab",
                                               help=f"{_("Audio bitrate in kbps.")} {_('If 0, let FFmpeg decide best bitrate.')}",
                                               callback=lambda x: check_positive_integer(x, allow_zero=True),
                                               )] = CONFIG.audio_bitrate,

    video_bitrate: Annotated[int, typer.Option("--video-bitrate", "-vb",
                                               help=f"{_("Video bitrate in kbps.")} {_('If 0, let FFmpeg decide best bitrate.')}",
                                               callback=lambda x: check_positive_integer(x, allow_zero=True),
                                               )] = CONFIG.video_bitrate,

    video_format: Annotated[str, typer.Option("--video-format", "-vf",
                                              help=f"{_("Video format.")} {_('Available formats:')} {", ".join(FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS)}",
                                              callback=lambda x: check_valid_options(x, FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS),
                                              )] = CONFIG.video_format,

    video_encoding_speed: Annotated[str, VideoEncodingSpeedOption(FFmpegBackend.ENCODING_SPEEDS)] = CONFIG.video_encoding_speed,

    video_quality: Annotated[str, VideoQualityOption(FFmpegBackend.QUALITY_PRESETS)] = CONFIG.video_quality,
    image_quality: Annotated[int, typer.Option("--image-quality", "-iq",
                                               help=_("Image quality (for ``image convert`` command). Valid values are between 1-100."),
                                               min=1, max=100,
                                               )] = CONFIG.image_quality,
    image_dpi: Annotated[int, typer.Option("--image-dpi", "-id",
                                           help=_("Image quality in dots per inch (DPI) (for ``image to_pdf`` command). Valid values are between 40-3600."),
                                           min=40, max=3600,
                                           )] = CONFIG.image_dpi,
    image_fit: Annotated[Img2PDFBackend.FitMode, typer.Option("--image-fit", "-if",
                                                              help=f'{_("Image fit (for ``image to_pdf`` command). Valid only if ``--page-size`` is defined. Valid values are")} {", ".join(mode.value for mode in Img2PDFBackend.FitMode)}.',
                                                              )] = Img2PDFBackend.FitMode(CONFIG.image_fit),

    image_page_size: Annotated[Img2PDFBackend.PageLayout | None, typer.Option("--image-page-size", "-ip",
                                                                              help=f'{_("Page size (for ``image to_pdf`` command). Valid values are: ")} {", ".join(mode.value for mode in Img2PDFBackend.PageLayout)}',
                                                                              )] = Img2PDFBackend.PageLayout(CONFIG.image_page_size) if CONFIG.image_page_size else None,

    image_resampling: Annotated[PillowBackend.ResamplingOption, typer.Option("--image-resampling", "-ir",
                                                                             help=f'{_("Resampling algorithm. Valid values are")} {", ".join(mode.value for mode in PillowBackend.ResamplingOption)}. {_("Defaults to")} {CONFIG.image_resampling}',
                                                                             )] = PillowBackend.ResamplingOption(CONFIG.image_resampling),

    pdf_compression: Annotated[str, typer.Option("--pdf-compression", "-pc",
                                                 help=f"{_('Compression level (high compression = low quality). Valid values are')} {', '.join(GhostscriptBackend.Compression.get_dict())}. {_('Defaults to')} {CONFIG.pdf_compression}.",
                                                 callback=lambda x: check_valid_options(x, GhostscriptBackend.Compression.get_dict()),
                                                 )] = CONFIG.pdf_compression,

    gui_zoom: Annotated[int, typer.Option("--gui-zoom", "-gz",
                                          help=_("GUI zoom level. Valid values are >= 1 (100 = normal size, 150 = 1.5x size, etc)."),
                                          min=1,
                                          )] = CONFIG.gui_zoom,

    gui_output_dir: Annotated[Path, typer.Option("--gui-output-dir", "-god",
                                                 help=f"{_('GUI output directory')}. {_('Defaults to')} {CONFIG.gui_output_dir}.",
                                                 callback=lambda x: check_dir_exists(x),
                                                 )] = Path(CONFIG.gui_output_dir),
):
    # update the configuration dictionary
    CONFIG.cache_enabled = cache_enabled
    CONFIG.cache_expire_after = cache_expire_after
    CONFIG.port = port
    CONFIG.language = language
    CONFIG.install_deps = None if install_deps == "None" or install_deps is None else bool(install_deps.capitalize())
    CONFIG.audio_bitrate = audio_bitrate
    CONFIG.video_bitrate = video_bitrate
    CONFIG.video_format = video_format
    CONFIG.video_encoding_speed = video_encoding_speed
    CONFIG.video_quality = video_quality
    CONFIG.image_quality = image_quality
    CONFIG.image_dpi = image_dpi
    CONFIG.image_fit = image_fit.value
    CONFIG.image_page_size = image_page_size.value if image_page_size else None
    CONFIG.image_resampling = image_resampling.value
    CONFIG.pdf_compression = pdf_compression
    CONFIG.gui_zoom = gui_zoom
    CONFIG.gui_output_dir = str(gui_output_dir.resolve())

    Configuration.set(CONFIG)
    Configuration.save()
    show_cmd.show()
    logger.info(f"{_('Configuration file')} {_('updated')}.")


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
