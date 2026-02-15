
# src\file_conversor\cli\video\execute_cmd.py
from pathlib import Path
from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    AudioBitrateOption,
    AudioCodecOption,
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
    VideoBitrateOption,
    VideoCodecOption,
)
from file_conversor.command.video import VideoExecuteCommand
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.system.win.ctx_menu import WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class VideoExecuteCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = VideoExecuteCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # no context menu for this command

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.execute,
            help=f"""
        {_('Execute FFmpeg command (advanced, use with caution).')}
    """,
            epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {group_name} {command_name} input_file.webm -od output_dir/ -f mp4 --audio-bitrate 192`

        - `file_conversor {group_name} {command_name} input_file.mp4 -f mp3 -fa "-c:a libmp3lame -pass 1"`
    """)

    def execute(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in VideoExecuteCommand.SupportedInFormats)],
        file_format: Annotated[VideoExecuteCommand.SupportedOutFormats, FormatOption()] = VideoExecuteCommand.SupportedOutFormats(CONFIG.video_format),

        audio_bitrate: Annotated[int | None, AudioBitrateOption()] = CONFIG.audio_bitrate,
        video_bitrate: Annotated[int | None, VideoBitrateOption()] = CONFIG.video_bitrate,

        audio_codec: Annotated[VideoExecuteCommand.AudioCodecs | None, AudioCodecOption()] = None,
        video_codec: Annotated[VideoExecuteCommand.VideoCodecs | None, VideoCodecOption()] = None,

        audio_filters: Annotated[list[str], typer.Option("--audio-filter", "-af",
                                                         help=f'{_("Apply a custom FFmpeg audio filter")} {_("(advanced option, use with caution). Uses the same format as FFmpeg filters (e.g., filter=option1=value1:option2=value2:...). Filters are applied in the order they appear in the command.")}. {_('Defaults to None (do not apply custom filters)')}.',
                                                         )] = [],  # noqa: B006
        video_filters: Annotated[list[str], typer.Option("--video-filter", "-vf",
                                                         help=f'{_("Apply a custom FFmpeg video filter")} {_("(advanced option, use with caution). Uses the same format as FFmpeg filters (e.g., filter=option1=value1:option2=value2:...). Filters are applied in the order they appear in the command.")}. {_('Defaults to None (do not apply custom filters)')}.',
                                                         )] = [],  # noqa: B006

        ffmpeg_args: Annotated[str, typer.Option("--ffmpeg-args", "-fa",
                                                 help=f'{_("Apply a custom FFmpeg output arguments (advanced option, use with caution).")}. {_('Defaults to None')}.',
                                                 )] = "",

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            VideoExecuteCommand.execute(
                input_files=input_files,
                file_format=file_format,
                audio_bitrate=audio_bitrate,
                video_bitrate=video_bitrate,
                audio_codec=audio_codec,
                video_codec=video_codec,
                audio_filters=audio_filters,
                video_filters=video_filters,
                ffmpeg_args=ffmpeg_args,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "VideoExecuteCLI",
]
