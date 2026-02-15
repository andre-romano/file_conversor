
# src\file_conversor\cli\audio\convert_cli.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    AudioBitrateOption,
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
)
from file_conversor.command import AudioConvertCommand
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win import WinContextCommand, WinContextMenu


# get app config
STATE = State.get()
CONFIG = Configuration.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AudioConvertCLI(AbstractTyperCommand):
    """Audio convert command class."""

    EXTERNAL_DEPENDENCIES = AudioConvertCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # FFMPEG commands
        icons_folder_path = Environment.get_icons_folder()
        for mode in AudioConvertCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="to_m4a",
                    description="To M4A",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f m4a "%1""',
                    icon=str(icons_folder_path / 'm4a.ico'),
                ),
                WinContextCommand(
                    name="to_mp3",
                    description="To MP3",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f mp3 "%1""',
                    icon=str(icons_folder_path / 'mp3.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=_('Convert a audio/video file to an audio format.'),
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.webm -f mp3 -od output_dir/ --audio-bitrate 192`
    - `file_conversor {group_name} {command_name} input_file.mp3 -f m4a`
""",
        )

    def convert(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in AudioConvertCommand.SupportedInFormats)],
        file_format: Annotated[AudioConvertCommand.SupportedOutFormats, FormatOption()],
        audio_bitrate: Annotated[int | None, AudioBitrateOption()] = CONFIG.audio_bitrate,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            AudioConvertCommand.convert(
                input_files=input_files,
                file_format=file_format,
                audio_bitrate=audio_bitrate,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "AudioConvertCLI",
]
