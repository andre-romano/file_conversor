
# src\file_conversor\cli\config_cmd.py

import typer

from typing import Annotated

from rich import print
from rich.pretty import Pretty

# user-provided modules
from file_conversor.config import Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.validators import check_is_bool_or_none, check_positive_integer, check_valid_options

# app configuration
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# create command
config_cmd = typer.Typer()


# config show
@config_cmd.command(help=f"""
    {_('Show the current configuration of the application')}.
""")
def show():
    print(f"{_('Configuration')}:", Pretty(CONFIG.to_dict(), expand_all=True))


# config set
@config_cmd.command(help=f"""
    {_('Configure the default options for the file converter.')}

    **{_('Example')}:** `file_conversor configure --video-bitrate 5000`
    **{_('Example')}:** `file_conversor configure --audio-bitrate 128`
""")
def set(
    language: Annotated[str, typer.Option("--language", "-l",
                                          help=_("Set preferred language for app (if available). Format lang_COUNTRY. Defaults to system preffered language or 'en_US' (English - United States)."),
                                          )] = CONFIG["language"],

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
                                           help=_("Image fit (for ``image to_pdf`` command). Valid only if ``--page-size`` is defined. Valid values are 'into', or 'fill'. Defaults to 'into'. "),
                                           callback=lambda x: check_valid_options(x.lower(), ['into', 'fill']),
                                           )] = CONFIG["image-fit"],

    image_page_size: Annotated[str | None, typer.Option("--image-page-size", "-ip",
                                                        help=_("Page size (for ``image to_pdf`` command). Format (width, height). Other valid values are: 'a4_portrait', 'a4_landscape'. Defaults to None (PDF size = image size)."),
                                                        callback=lambda x: check_valid_options(x.lower() if x else None, [None, 'a4', 'a4_landscape']),
                                                        )] = CONFIG["image-page-size"],

    image_set_metadata: Annotated[bool, typer.Option("--image-set-metadata", "-is",
                                                     help=_("Set PDF metadata (for ``image to_pdf`` command). Defaults to True (set creator, producer, modification date, etc)."),
                                                     callback=check_is_bool_or_none,
                                                     is_flag=True,
                                                     )] = CONFIG["image-set-metadata"],

    pdf_compression: Annotated[str, typer.Option("--pdf-compression", "-pc",
                                                 help=f"{_('Compression level (high compression = low quality). Valid values are')} {', '.join(["low", "medium", "high", "none"])}. {_('Defaults to')} {CONFIG["pdf-compression"]}.",
                                                 callback=lambda x: check_valid_options(x, ["low", "medium", "high", "none"]),
                                                 )] = CONFIG["pdf-compression"],

    pdf_preset: Annotated[str, typer.Option("--pdf-preset", "-pp",
                                            help=f"{_('Compatibility preset. Valid values are')} '1.3', '1.4', ..., '1.7' . {_('Defaults to')} {CONFIG["pdf-preset"]}.",
                                            callback=lambda x: check_valid_options(x, ["1.3", "1.4", "1.5", "1.6", "1.7"]),
                                            )] = CONFIG["pdf-preset"],
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
        "image-set-metadata": image_set_metadata,
        "pdf-compression": pdf_compression,
        "pdf-preset": pdf_preset,
    })
    CONFIG.save()
    show()
    logger.info(f"{_('Configuration file')} {_('updated')}.")
