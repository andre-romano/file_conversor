
# src\file_conversor\cli\doc\convert_cli.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
)
from file_conversor.command.doc import DocConvertCommand
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class DocConvertCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = DocConvertCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # WordBackend commands
        icons_folder_path = Environment.get_icons_folder()
        for mode in DocConvertCommand.SupportedInFormats:
            ext_in = mode.value
            ctx_menu.add_extension(f".{ext_in}", [
                WinContextCommand(
                    name=f"to_{mode.value}",
                    description=f"To {mode.value.upper()}",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -f "{mode.value}""',
                    icon=str(icons_folder_path / f"{mode.value}.ico"),
                )
                for mode in DocConvertCommand.SupportedOutFormats
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=_('Convert document files into other formats (requires LibreOffice).'),
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.odt -f doc`

    - `file_conversor {group_name} {command_name} input_file.docx -f pdf`

    - `file_conversor {group_name} {command_name} input_file.pdf -f docx`
""")

    def convert(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in DocConvertCommand.SupportedInFormats)],
        file_format: Annotated[DocConvertCommand.SupportedOutFormats, FormatOption()],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        """Convert document files into other formats."""
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            DocConvertCommand.convert(
                input_files=input_files,
                file_format=file_format,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "DocConvertCLI",
]
