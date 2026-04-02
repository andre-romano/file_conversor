
# src\file_conversor\cli\config\set_cli.py

from typing import Annotated

import typer

from rich import print
from rich.pretty import Pretty

from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import VideoEncodingSpeedOption, VideoQualityOption
from file_conversor.command.config import ConfigSetCommand
from file_conversor.command.config.set_cmd import (
    ConfigSetAudioOutFormat,
    ConfigSetImageFitMode,
    ConfigSetImagePageLayout,
    ConfigSetImageResamplingOption,
    ConfigSetPdfCompression,
    ConfigSetVideoEncoding,
    ConfigSetVideoOutFormat,
    ConfigSetVideoQuality,
)
from file_conversor.config import (
    AVAILABLE_LANGUAGES,
    Configuration,
    Log,
    get_translation,
    locale,
)
from file_conversor.utils.validators import (
    check_is_bool_or_none,
    check_valid_options,
)


# app configuration
CONFIG = Configuration.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ConfigSetCLI(AbstractTyperCommand):
    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.set,
            help=_('Configure the default options for the app.'),
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor configure --video-bitrate 5000`

    - `file_conversor configure --audio-bitrate 128`
""")

    def set(
        self,
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
                                              callback=lambda x: check_valid_options(x, AVAILABLE_LANGUAGES),  # pyright: ignore[reportUnknownArgumentType]
                                              )] = locale.normalize_lang_code(CONFIG.language) or locale.get_default_language(),

        install_deps: Annotated[str | None, typer.Option("--install-deps", "-install",
                                                         help=_("Install missing external dependencies action. 'True' for auto install. 'False' to not install missing dependencies."),
                                                         callback=check_is_bool_or_none,
                                                         )] = str(CONFIG.install_deps),

        audio_bitrate: Annotated[int | None, typer.Option("--audio-bitrate", "-ab",
                                                          help=f"{_("Audio bitrate in kbps.")} {_('If 0, let FFmpeg decide best bitrate.')}",
                                                          min=-1,
                                                          )] = CONFIG.audio_bitrate,

        video_bitrate: Annotated[int | None, typer.Option("--video-bitrate", "-vb",
                                                          help=f"{_("Video bitrate in kbps.")} {_('If 0, let FFmpeg decide best bitrate.')}",
                                                          min=-1,
                                                          )] = CONFIG.video_bitrate,

        audio_format: Annotated[ConfigSetAudioOutFormat, typer.Option("--audio-format", "-af",
                                                                      help=f"{_("Default audio format.")}",
                                                                      )] = ConfigSetAudioOutFormat(CONFIG.audio_format),

        video_format: Annotated[ConfigSetVideoOutFormat, typer.Option("--video-format", "-vf",
                                                                      help=f"{_("Default video format.")}",
                                                                      )] = ConfigSetVideoOutFormat(CONFIG.video_format),

        video_encoding_speed: Annotated[ConfigSetVideoEncoding, VideoEncodingSpeedOption()] = ConfigSetVideoEncoding(CONFIG.video_encoding_speed),
        video_quality: Annotated[ConfigSetVideoQuality, VideoQualityOption()] = ConfigSetVideoQuality(CONFIG.video_quality),
        image_quality: Annotated[int, typer.Option("--image-quality", "-iq",
                                                   help=_("Image quality (for ``image convert`` command). Valid values are between 1-100."),
                                                   min=1, max=100,
                                                   )] = CONFIG.image_quality,
        image_dpi: Annotated[int, typer.Option("--image-dpi", "-id",
                                               help=_("Image quality in dots per inch (DPI) (for ``image to_pdf`` command). Valid values are between 40-3600."),
                                               min=40, max=3600,
                                               )] = CONFIG.image_dpi,
        image_fit: Annotated[ConfigSetImageFitMode, typer.Option("--image-fit", "-if",
                                                                 help=f'{_("Image fit (for ``image to_pdf`` command). Valid only if ``--page-size`` is defined. ")}.',
                                                                 )] = ConfigSetImageFitMode(CONFIG.image_fit),

        image_page_size: Annotated[ConfigSetImagePageLayout, typer.Option("--image-page-size", "-ip",
                                                                          help=f'{_("Page size (for ``image to_pdf`` command). ")} ',
                                                                          )] = ConfigSetImagePageLayout(CONFIG.image_page_size),

        image_resampling: Annotated[ConfigSetImageResamplingOption, typer.Option("--image-resampling", "-ir",
                                                                                 help=f'{_("Resampling algorithm.")} {_("Defaults to")} {CONFIG.image_resampling}',
                                                                                 )] = ConfigSetImageResamplingOption(CONFIG.image_resampling),

        pdf_compression: Annotated[ConfigSetPdfCompression, typer.Option("--pdf-compression", "-pc",
                                                                         help=f"{_('Compression level (high compression = low quality).')} {_('Defaults to')} {CONFIG.pdf_compression}.",
                                                                         )] = ConfigSetPdfCompression(CONFIG.pdf_compression),
    ):
        # update the configuration dictionary
        command = ConfigSetCommand(
            cache_enabled=cache_enabled,
            cache_expire_after=cache_expire_after,
            language=language,
            install_deps=bool(install_deps) if isinstance(install_deps, str) else None,
            audio_bitrate=audio_bitrate,
            video_bitrate=video_bitrate,
            audio_format=audio_format.value,
            video_format=video_format.value,
            video_encoding_speed=video_encoding_speed.value,
            video_quality=video_quality.value,
            image_quality=image_quality,
            image_dpi=image_dpi,
            image_fit=image_fit.value,
            image_page_size=image_page_size.value,
            image_resampling=image_resampling.value,
            pdf_compression=pdf_compression.value,
        )
        command.execute()
        print(f"{_('Configuration')}:", Pretty(command.to_dict(), expand_all=True))


__all__ = [
    "ConfigSetCLI",
]
