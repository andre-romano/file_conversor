
# src\file_conversor\cli\pdf\split_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    InputFilesArgument,
    OutputDirOption,
    PasswordOption,
)
from file_conversor.command.pdf import PdfSplitCommand
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


class PdfSplitCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PdfSplitCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for mode in PdfSplitCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="split",
                    description="Split",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / 'split.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.split,
            help=f"""
    {_('Split PDF pages into several 1-page PDFs.')}

    {_('For every PDF page, a new single page PDF will be created using the format `input_file_X.pdf`, where X is the page number.')}
""",
            epilog=f"""
    **{_('Examples')}:** 



    *{_('Split pages of input_file.pdf into output_file_X.pdf files')}*:

    - `file_conversor {group_name} {command_name} input_file.pdf -od D:/Downloads` 



    *{_('For every PDF page, generate a "input_file_X.pdf" file')}*:

    - `file_conversor {group_name} {command_name} input_file.pdf` 
""")

    def split(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in PdfSplitCommand.SupportedInFormats)],
        password: Annotated[str, PasswordOption()] = "",
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            PdfSplitCommand.split(
                input_files=input_files,
                password=password,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "PdfSplitCLI",
]
