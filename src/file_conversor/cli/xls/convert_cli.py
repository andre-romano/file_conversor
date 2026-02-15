
# src\file_conversor\cli\xls\convert_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
)
from file_conversor.command.xls import XlsConvertCommand
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


class XlsConvertCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = XlsConvertCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # WordBackend commands
        for mode in XlsConvertCommand.SupportedInFormats:
            ext_in = mode.value
            ctx_menu.add_extension(f".{ext_in}", [
                WinContextCommand(
                    name=f"to_{mode.value}",
                    description=f"To {mode.value.upper()}",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f "{mode.value}" "%1""',
                    icon=str(icons_folder_path / f"{mode.value}.ico"),
                )
                for mode in XlsConvertCommand.SupportedOutFormats
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=f"""
    {_('Convert spreadsheet files into other formats (requires LibreOffice).')}
""",
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.ods -f xls`

    - `file_conversor {group_name} {command_name} input_file.xlsx -f pdf`
""")

    def convert(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in XlsConvertCommand.SupportedInFormats)],
        file_format: Annotated[XlsConvertCommand.SupportedOutFormats, FormatOption()],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            XlsConvertCommand.convert(
                input_files=input_files,
                file_format=file_format,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "XlsConvertCLI",
]
