
# src\file_conversor\cli\pdf\convert_cmd.py

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import DPIOption, FormatOption, InputFilesArgument, OutputDirOption, PasswordOption

from file_conversor.backend.pdf import PyMuPDFBackend, PDF2DOCXBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils.formatters import format_in_out_files_tuple

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfConvertTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = {
        *PyMuPDFBackend.EXTERNAL_DEPENDENCIES,
        *PDF2DOCXBackend.EXTERNAL_DEPENDENCIES,
    }

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for ext in PyMuPDFBackend.SUPPORTED_IN_FORMATS:
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
            ])
        for ext in PDF2DOCXBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
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
    {_('Convert a PDF file to a different format (might require LibreOffice).')}
    
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
        input_files: Annotated[List[Path], InputFilesArgument({
            **PyMuPDFBackend.SUPPORTED_IN_FORMATS,
            **PDF2DOCXBackend.SUPPORTED_IN_FORMATS,
        })],
        format: Annotated[str, FormatOption({
            **PyMuPDFBackend.SUPPORTED_OUT_FORMATS,
            **PDF2DOCXBackend.SUPPORTED_OUT_FORMATS,
        })],
        dpi: Annotated[int, DPIOption()] = CONFIG.image_dpi,
        password: Annotated[str | None, PasswordOption()] = None,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with ProgressManagerRich(len(input_files)) as progress_mgr:
            files = format_in_out_files_tuple(
                input_files=input_files,
                output_dir=output_dir,
                file_format=format,
                overwrite_output=STATE.overwrite_output.enabled,
            )
            logger.info(f"[bold]{_('Converting files')}[/] ...")
            # Perform conversion
            if format in PyMuPDFBackend.SUPPORTED_OUT_FORMATS:
                backend = PyMuPDFBackend(verbose=STATE.loglevel.get().is_verbose())
                for input_file, output_file in files:
                    backend.convert(
                        input_file=input_file,
                        output_file=output_file,
                        dpi=dpi,
                        password=password,
                    )
            else:
                backend = PDF2DOCXBackend(verbose=STATE.loglevel.get().is_verbose())
                for input_file, output_file in files:
                    backend.convert(
                        input_file=input_file,
                        output_file=output_file,
                        password=password,
                    )
            progress_mgr.complete_step()

        logger.info(f"{_('File convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "PdfConvertTyperCommand",
]
