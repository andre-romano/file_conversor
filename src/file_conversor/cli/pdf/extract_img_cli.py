
# src\file_conversor\cli\pdf\extract_img_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption
from file_conversor.command.pdf import PdfExtractImgCommand
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


class PdfExtractImgCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PdfExtractImgCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for mode in PdfExtractImgCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="extract_img",
                    description="Extract IMG",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / 'separate.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.extract_img,
            help=f"""
    {_('Extract images from a PDF.')}
    
    {_('For every PDF page, a new image file will be created using the format `input_file_X`, where X is the page number.')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.pdf -od D:/Downloads` 
""")

    def extract_img(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in PdfExtractImgCommand.SupportedInFormats)],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            PdfExtractImgCommand.extract_img(
                input_files=input_files,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "PdfExtractImgCLI",
]
