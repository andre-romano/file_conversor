
# src\file_conversor\cli\ebook\convert_cli.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
)
from file_conversor.command.ebook import EbookConvertCommand, EbookConvertOutFormats
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


class EbookConvertCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # FFMPEG commands
        icons_folder_path = Environment.get_icons_folder()
        for ext_in in EbookConvertCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                WinContextCommand(
                    name=f"to_{ext_out}",
                    description=f"To {ext_out.upper()}",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -f "{ext_out}""',
                    icon=str(icons_folder_path / f"{ext_out}.ico"),
                )
                for ext_out in EbookConvertCommand.get_out_formats()
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=_('Convert an ebook file to another ebook format or PDF (requires Calibre).'),
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.epub -f pdf -od output_dir/`
    - `file_conversor {group_name} {command_name} input_file.mobi -f epub`
""")

    def convert(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(EbookConvertCommand.get_in_formats())],
        file_format: Annotated[EbookConvertOutFormats, FormatOption()],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        """Execute ebook conversion command."""
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = EbookConvertCommand(
                input_files=input_files,
                file_format=file_format,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "EbookConvertCLI",
]
