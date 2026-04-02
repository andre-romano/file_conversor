
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
from file_conversor.command.pdf.convert_cmd import PdfConvertOutFormats
from file_conversor.config import (
    Configuration,
    Log,
    State,
    get_translation,
)
from file_conversor.system import ContextMenu, ContextMenuItem


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfConvertCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        for ext_in in PdfConvertCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name=f"to_{ext_out}",
                    description=f"To {ext_out.upper()}",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-f", ext_out],
                    icon=icons_folder / f'{ext_out}.ico',
                )
                for ext_out in ["png", "jpg", "docx"]
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
        input_files: Annotated[list[Path], InputFilesArgument(PdfConvertCommand.get_in_formats())],
        file_format: Annotated[PdfConvertOutFormats, FormatOption()],
        dpi: Annotated[int, DPIOption()] = CONFIG.image_dpi,
        password: Annotated[str, PasswordOption()] = "",
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = PdfConvertCommand(
                input_files=input_files,
                file_format=file_format,
                dpi=dpi,
                password=password,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "PdfConvertCLI",
]
