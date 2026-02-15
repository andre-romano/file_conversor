
# src\file_conversor\cli\config\set_cli.py

from pathlib import Path
from typing import Annotated, override

import typer

from rich.pretty import Pretty

from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import VideoEncodingSpeedOption, VideoQualityOption
from file_conversor.command.config import ConfigSetCommand
from file_conversor.config import (
    AVAILABLE_LANGUAGES,
    Configuration,
    Log,
    get_translation,
    locale,
)
from file_conversor.system.win.ctx_menu import WinContextMenu
from file_conversor.utils.validators import (
    check_dir_exists,
    check_is_bool_or_none,
    check_valid_options,
)


# app configuration
CONFIG = Configuration.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ConfigSetCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = ConfigSetCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # no context menu for this command

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
                                                         help=_("Install missing external dependencies action. 'True' for auto install. 'False' to not install missing dependencies. 'None' to ask user for action."),
                                                         callback=check_is_bool_or_none,
                                                         )] = str(CONFIG.install_deps),

        port: Annotated[int, typer.Option("--port", "-p",
                                          help=f'{_("Set preferred listen port for app (if available). Ports below 1024 require root privileges. Defaults to 5000.")}.',
                                          min=1, max=65535,
                                          )] = CONFIG.api_port,

        audio_bitrate: Annotated[int | None, typer.Option("--audio-bitrate", "-ab",
                                                          help=f"{_("Audio bitrate in kbps.")} {_('If 0, let FFmpeg decide best bitrate.')}",
                                                          min=-1,
                                                          )] = CONFIG.audio_bitrate,

        video_bitrate: Annotated[int | None, typer.Option("--video-bitrate", "-vb",
                                                          help=f"{_("Video bitrate in kbps.")} {_('If 0, let FFmpeg decide best bitrate.')}",
                                                          min=-1,
                                                          )] = CONFIG.video_bitrate,

        audio_format: Annotated[ConfigSetCommand.AudioOutFormat, typer.Option("--audio-format", "-af",
                                                                              help=f"{_("Default audio format.")}",
                                                                              )] = ConfigSetCommand.AudioOutFormat(CONFIG.audio_format),

        video_format: Annotated[ConfigSetCommand.VideoOutFormat, typer.Option("--video-format", "-vf",
                                                                              help=f"{_("Default video format.")}",
                                                                              )] = ConfigSetCommand.VideoOutFormat(CONFIG.video_format),

        video_encoding_speed: Annotated[ConfigSetCommand.VideoEncoding, VideoEncodingSpeedOption(CONFIG.video_encoding_speed)] = ConfigSetCommand.VideoEncoding(CONFIG.video_encoding_speed),
        video_quality: Annotated[ConfigSetCommand.VideoQuality, VideoQualityOption(CONFIG.video_quality)] = ConfigSetCommand.VideoQuality(CONFIG.video_quality),
        image_quality: Annotated[int, typer.Option("--image-quality", "-iq",
                                                   help=_("Image quality (for ``image convert`` command). Valid values are between 1-100."),
                                                   min=1, max=100,
                                                   )] = CONFIG.image_quality,
        image_dpi: Annotated[int, typer.Option("--image-dpi", "-id",
                                               help=_("Image quality in dots per inch (DPI) (for ``image to_pdf`` command). Valid values are between 40-3600."),
                                               min=40, max=3600,
                                               )] = CONFIG.image_dpi,
        image_fit: Annotated[ConfigSetCommand.ImageFitMode, typer.Option("--image-fit", "-if",
                                                                         help=f'{_("Image fit (for ``image to_pdf`` command). Valid only if ``--page-size`` is defined. ")}.',
                                                                         )] = ConfigSetCommand.ImageFitMode(CONFIG.image_fit),

        image_page_size: Annotated[ConfigSetCommand.ImagePageLayout, typer.Option("--image-page-size", "-ip",
                                                                                  help=f'{_("Page size (for ``image to_pdf`` command). ")} ',
                                                                                  )] = ConfigSetCommand.ImagePageLayout(CONFIG.image_page_size),

        image_resampling: Annotated[ConfigSetCommand.ImageResamplingOption, typer.Option("--image-resampling", "-ir",
                                                                                         help=f'{_("Resampling algorithm. Valid values are")} {", ".join(mode.value for mode in ConfigSetCommand.ImageResamplingOption)}. {_("Defaults to")} {CONFIG.image_resampling}',
                                                                                         )] = ConfigSetCommand.ImageResamplingOption(CONFIG.image_resampling),

        pdf_compression: Annotated[ConfigSetCommand.PdfCompression, typer.Option("--pdf-compression", "-pc",
                                                                                 help=f"{_('Compression level (high compression = low quality). Valid values are')} {', '.join(mode.value for mode in ConfigSetCommand.PdfCompression)}. {_('Defaults to')} {CONFIG.pdf_compression}.",
                                                                                 )] = ConfigSetCommand.PdfCompression(CONFIG.pdf_compression),

        gui_zoom: Annotated[int, typer.Option("--gui-zoom", "-gz",
                                              help=_("GUI zoom level. Valid values are >= 1 (100 = normal size, 150 = 1.5x size, etc)."),
                                              min=1,
                                              )] = CONFIG.gui_zoom,

        gui_output_dir: Annotated[Path, typer.Option("--gui-output-dir", "-god",
                                                     help=f"{_('GUI output directory')}. {_('Defaults to')} {CONFIG.gui_output_dir}.",
                                                     callback=check_dir_exists,  # pyright: ignore[reportUnknownArgumentType]
                                                     )] = Path(CONFIG.gui_output_dir),
    ):
        # update the configuration dictionary
        ConfigSetCommand.set(
            cache_enabled=cache_enabled,
            cache_expire_after=cache_expire_after,
            language=language,
            install_deps=install_deps,
            port=port,
            audio_bitrate=audio_bitrate,
            video_bitrate=video_bitrate,
            audio_format=audio_format,
            video_format=video_format,
            video_encoding_speed=video_encoding_speed,
            video_quality=video_quality,
            image_quality=image_quality,
            image_dpi=image_dpi,
            image_fit=image_fit,
            image_page_size=image_page_size,
            image_resampling=image_resampling,
            pdf_compression=pdf_compression,
            gui_zoom=gui_zoom,
            gui_output_dir=gui_output_dir,
        )
        print(f"{_('Configuration')}:", Pretty(CONFIG.to_dict(), expand_all=True))


__all__ = [
    "ConfigSetCLI",
]
