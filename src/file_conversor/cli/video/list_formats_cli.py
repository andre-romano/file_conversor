
# src\file_conversor\cli\video\list_formats_cmd.py

from typing import Annotated, override

# CLI
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import FormatOption

# COMMAND
from file_conversor.command.video import VideoListFormatsCommand

# CORE
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.system.win.ctx_menu import WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoListFormatsCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = VideoListFormatsCommand.EXTERNAL_DEPENDENCIES

    @override
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
        file_format: Annotated[VideoListFormatsCommand.SupportedOutFormats | None, FormatOption()] = None,
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            data_list = VideoListFormatsCommand.list_formats(
                desired_format=file_format,
                progress_callback=task.update,
            )
            for data in data_list:
                logger.info(f"[bold]Format:[/bold] {data.file_format.upper()}")
                logger.info(f"  - {_('Audio codecs')}: {', '.join(data.audio_codecs)}")
                logger.info(f"  - {_('Video codecs')}: {', '.join(data.video_codecs)}")
                print()  # add a final newline


__all__ = [
    "VideoListFormatsCLI",
]
