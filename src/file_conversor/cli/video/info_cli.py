
# src\file_conversor\cli\video\info_cmd.py

from pathlib import Path
from typing import Annotated, override

from rich import print
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument
from file_conversor.command.video import (
    VideoInfoChapter,
    VideoInfoCommand,
    VideoInfoStream,
)
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win import WinContextCommand, WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoInfoCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # FFMPEG commands
        icons_folder_path = Environment.get_icons_folder()
        for ext_in in VideoInfoCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                WinContextCommand(
                    name="info",
                    description="Get Info",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / 'info.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.info,
            help=f"""
    {_('Get information about a video file.')}

    {_('This command retrieves metadata and other information about the video file')}:

    - {_('Format')} (avi, mp4, mov, etc)

    - {_('Duration')} (HH:MM:SS)

    - {_('Other properties')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} filename.webm`

    - `file_conversor {group_name} {command_name} other_filename.mp4`
""")

    def info(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(VideoInfoCommand.get_in_formats())],
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = VideoInfoCommand(
                input_files=input_files,
                progress_callback=task.update,
            )
            command.execute()

            for data in command.output:
                group = Group(
                    Text(f"📁 {_('File Information')}:", style="bold cyan"),
                    f"  - {_('Name')}: {data.filename.name}",
                    f"  - {_('Format')}: {data.format_info.file_format}",
                    f"  - {_('Duration')}: {data.format_info.duration}",
                    f"  - {_('Size')}: {data.format_info.size}",
                    f"  - {_('Bitrate')}: {data.format_info.bitrate}",
                    f"\n",
                    Text(f"🎬 {_("Media Streams")}:", style="bold yellow"),
                    *self._get_stream_info(data.streams),
                    f"\n",
                    Text(f"📖 {_('Chapters')}:", style="bold green"),
                    *self._get_chapters_info(data.chapters),
                )
                print(Panel(group, title=f"🧾 {_('File Analysis')}", border_style="blue"))

    def _get_stream_info(self, streams: list[VideoInfoStream]) -> list[RenderableType]:
        output_text: list[RenderableType] = []
        for idx, stream in enumerate(streams):
            output_text.extend([
                Text(f"\n  🔹 {_('Stream')} #{idx} ({stream.type}):"),
                f"    - {_('Codec')}: {stream.codec}",
                f"    - {_('Bitrate')}: {stream.bitrate}",
                f"    - {_('Resolution')}: {stream.resolution}" if stream.resolution else "",
                f"    - {_('Sampling rate')}: {stream.sample_rate}" if stream.sample_rate else "",
                f"    - {_('Channels')}: {stream.channels}" if stream.channels else "",
            ])
        return output_text

    def _get_chapters_info(self, chapters: list[VideoInfoChapter]) -> list[RenderableType]:
        output_text: list[RenderableType] = []
        for chapter in chapters:
            output_text.extend([
                f"  - {chapter.title} ({_('Time')}: {chapter.start_time})",
            ])
        return output_text


__all__ = [
    "VideoInfoCLI",
]
