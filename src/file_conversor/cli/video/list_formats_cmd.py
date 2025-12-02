
# src\file_conversor\cli\video\list_formats_cmd.py

import typer

from rich import print

from typing import Annotated, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend

from file_conversor.cli.video._typer import OTHERS_PANEL as RICH_HELP_PANEL
from file_conversor.cli.video._typer import COMMAND_NAME, LIST_FORMATS_NAME

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.validators import check_valid_options
from file_conversor.utils.typer_utils import FormatOption

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES


@typer_cmd.command(
    name=LIST_FORMATS_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('List available video formats and codecs.')}

        {_('If a video format is provided, only codecs for that format will be shown.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {LIST_FORMATS_NAME}`

        - `file_conversor {COMMAND_NAME} {LIST_FORMATS_NAME} -f avi`
    """)
def list_formats(
    file_format: Annotated[str | None, FormatOption(FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS)] = None,
):
    format_dict = FFmpegBackend.SUPPORTED_OUT_FORMATS
    if file_format:
        format_dict = {file_format: format_dict[file_format]}

    for fmt, fmt_info in format_dict.items():
        args, kwargs = fmt_info
        logger.info(f"[bold]{fmt}[/bold]")
        logger.info(f"  - {_('Audio codecs')}: {', '.join(kwargs['available_audio_codecs'])}")
        logger.info(f"  - {_('Video codecs')}: {', '.join(kwargs['available_video_codecs'])}")
    print()  # add a final newline


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
]
