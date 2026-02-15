
# src\file_conversor\cli\pdf\convert_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    DPIOption,
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
    PasswordOption,
)
from file_conversor.command import PdfConvertCommand
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


class PdfConvertCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PdfConvertCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for mode in PdfConvertCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="to_png",
                    description="To PNG",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -f "png""',
                    icon=str(icons_folder_path / 'png.ico'),
                ),
                WinContextCommand(
                    name="to_jpg",
                    description="To JPG",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -f "jpg""',
                    icon=str(icons_folder_path / 'jpg.ico'),
                ),
                WinContextCommand(
                    name="to_docx",
                    description="To DOCX",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -f "docx""',
                    icon=str(icons_folder_path / 'docx.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=f"""
    {_('Convert a PDF file to a different format.')}
    
    {_('Outputs a file with the PDF page number at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.pdf -f jpg --dpi 200`

    - `file_conversor {group_name} {command_name} input_file.pdf -f png`

    - `file_conversor {group_name} {command_name} input_file.pdf -f docx`
""")

    def convert(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in PdfConvertCommand.SupportedInFormats)],
        file_format: Annotated[PdfConvertCommand.SupportedOutFormats, FormatOption()],
        dpi: Annotated[int, DPIOption()] = CONFIG.image_dpi,
        password: Annotated[str, PasswordOption()] = "",
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            PdfConvertCommand.convert(
                input_files=input_files,
                file_format=file_format,
                dpi=dpi,
                password=password,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "PdfConvertCLI",
]
