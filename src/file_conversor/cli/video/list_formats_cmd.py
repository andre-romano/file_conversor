
# src\file_conversor\cli\video\list_formats_cmd.py

from typing import Annotated, Iterable, List
from pathlib import Path

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand
from file_conversor.cli._utils.typer import FormatOption

from file_conversor.backend import FFmpegBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoListFormatsTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # no context menu for this command

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.list_formats,
            help=f"""
    {_('List available video formats and codecs.')}

    {_('If a video format is provided, only codecs for that format will be shown.')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name}`

    - `file_conversor {group_name} {command_name} -f avi`
""")

    def list_formats(
        self,
        file_format: Annotated[str | None, FormatOption(FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS)] = None,
    ):
        format_dict = FFmpegBackend.SUPPORTED_OUT_FORMATS
        if file_format:
            format_dict = {file_format: format_dict[file_format]}

        for fmt, fmt_info in format_dict.items():
            logger.info(f"[bold]{fmt}[/bold]")
            logger.info(f"  - {_('Audio codecs')}: {', '.join(fmt_info.kwargs['available_audio_codecs'])}")
            logger.info(f"  - {_('Video codecs')}: {', '.join(fmt_info.kwargs['available_video_codecs'])}")
        print()  # add a final newline


__all__ = [
    "VideoListFormatsTyperCommand",
]
