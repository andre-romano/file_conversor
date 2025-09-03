
# src\file_conversor\cli\config\set_cmd.py

import typer

from typing import Annotated

from rich import print

# user-provided modules
from file_conversor.cli.config._typer import COMMAND_NAME, SET_NAME
import file_conversor.cli.config.show_cmd as show_cmd

from file_conversor.backend import Img2PDFBackend, PillowBackend
from file_conversor.config import Configuration, State, Log, locale, get_translation, get_available_languages

from file_conversor.utils.validators import check_is_bool_or_none, check_positive_integer, check_valid_options

# app configuration
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# create command
typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = set()


@typer_cmd.command(
    name=SET_NAME,
    help=f"""
        {_('Configure the default options for the file converter.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor configure --video-bitrate 5000`

        - `file_conversor configure --audio-bitrate 128`
    """,
)
def set(
    language: Annotated[str, typer.Option("--language", "-l",
                                          help=f'{_("Set preferred language for app (if available). Available languages:")} {", ".join(get_available_languages())}. {_("Defaults to system preffered language or 'en_US' (English - United States)")}.',
                                          callback=lambda x: check_valid_options(x, get_available_languages()),
                                          )] = locale.normalize_lang_code(CONFIG["language"]) or locale.get_default_language(),

    install_deps: Annotated[str | None, typer.Option("--install-deps", "-install",
                                                     help=_("Install missing external dependencies action. 'True' for auto install. 'False' to not install missing dependencies. 'None' to ask user for action."),
                                                     callback=check_is_bool_or_none,
                                                     )] = CONFIG["install-deps"],

    audio_bitrate: Annotated[int, typer.Option("--audio-bitrate", "-ab",
                                               help=_("Audio bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["audio-bitrate"],

    video_bitrate: Annotated[int, typer.Option("--video-bitrate", "-vb",
                                               help=_("Video bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["video-bitrate"],

    image_quality: Annotated[int, typer.Option("--image-quality", "-iq",
                                               help=_("Image quality (for ``image convert`` command). Valid values are between 1-100."),
                                               min=1, max=100,
                                               )] = CONFIG["image-quality"],

    image_dpi: Annotated[int, typer.Option("--image-dpi", "-id",
                                           help=_("Image quality in dots per inch (DPI) (for ``image to_pdf`` command). Valid values are between 40-3600."),
                                           min=40, max=3600,
                                           )] = CONFIG["image-dpi"],

    image_fit: Annotated[str, typer.Option("--image-fit", "-if",
                                           help=f'{_("Image fit (for ``image to_pdf`` command). Valid only if ``--page-size`` is defined. Valid values are")} {", ".join(Img2PDFBackend.FIT_MODES)}',
                                           callback=lambda x: check_valid_options(x.lower(), ['into', 'fill']),
                                           )] = CONFIG["image-fit"],

    image_page_size: Annotated[str | None, typer.Option("--image-page-size", "-ip",
                                                        help=f'{_("Page size (for ``image to_pdf`` command). Format (width, height). Other valid values are:")} {", ".join(Img2PDFBackend.PAGE_LAYOUT)}',
                                                        callback=lambda x: check_valid_options(x.lower() if x else None, Img2PDFBackend.PAGE_LAYOUT),
                                                        )] = CONFIG["image-page-size"],

    image_resampling: Annotated[str, typer.Option("--image-resampling", "-ir",
                                                  help=f'{_("Resampling algorithm. Valid values are")} {", ".join(PillowBackend.RESAMPLING_OPTIONS)}. {_("Defaults to")} {CONFIG["image-resampling"]}',
                                                  callback=lambda x: check_valid_options(x, PillowBackend.RESAMPLING_OPTIONS),
                                                  )] = CONFIG["image-resampling"],

    pdf_compression: Annotated[str, typer.Option("--pdf-compression", "-pc",
                                                 help=f"{_('Compression level (high compression = low quality). Valid values are')} {', '.join(["low", "medium", "high", "none"])}. {_('Defaults to')} {CONFIG["pdf-compression"]}.",
                                                 callback=lambda x: check_valid_options(x, ["low", "medium", "high", "none"]),
                                                 )] = CONFIG["pdf-compression"],
):
    # update the configuration dictionary
    CONFIG.update({
        "language": language,
        "install-deps": None if install_deps == "None" or install_deps is None else bool(install_deps),
        "audio-bitrate": audio_bitrate,
        "video-bitrate": video_bitrate,
        "image-quality": image_quality,
        "image-dpi": image_dpi,
        "image-fit": image_fit,
        "image-page-size": image_page_size,
        "image-resampling": image_resampling,
        "pdf-compression": pdf_compression,
    })
    CONFIG.save()
    show_cmd.show()
    logger.info(f"{_('Configuration file')} {_('updated')}.")
