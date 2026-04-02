
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
from file_conversor.command import AudioConvertCommand, AudioConvertOutFormats
from file_conversor.config import (
    Configuration,
    Log,
    State,
    get_translation,
)
from file_conversor.system import ContextMenu, ContextMenuItem


# get app config
STATE = State.get()
CONFIG = Configuration.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AudioConvertCLI(AbstractTyperCommand):
    """Audio convert command class."""
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        # FFMPEG commands
        for ext_in in AudioConvertCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name=f"to_{ext_out}",
                    description=f"To {ext_out.upper()}",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-f", ext_out],
                    icon=icons_folder / f'{ext_out}.ico',
                )
                for ext_out in ["mp3", "m4a"]
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
        input_files: Annotated[list[Path], InputFilesArgument(AudioConvertCommand.get_in_formats())],
        file_format: Annotated[AudioConvertOutFormats, FormatOption()],
        audio_bitrate: Annotated[int | None, AudioBitrateOption()] = CONFIG.audio_bitrate,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = AudioConvertCommand(
                input_files=input_files,
                file_format=file_format,
                audio_bitrate=audio_bitrate,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "AudioConvertCLI",
]
