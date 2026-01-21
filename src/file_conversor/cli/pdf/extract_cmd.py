
# src\file_conversor\cli\pdf\extract_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List, Iterable

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption, PasswordOption

from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils.formatters import parse_pdf_pages

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfExtractTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PyPDFBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for ext in PyPDFBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="extract",
                    description="Extract",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / 'extract.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.extract,
            help=f"""
    {_('Extract specific pages from a PDF.')}
    
    {_('Outputs a file with _extracted at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 



    *{_('Extract pages 1 to 2, 4 and 6')}*:

    - `file_conversor {group_name} {command_name} input_file.pdf -pg 1-2 -pg 4-4 -pg 6-6 -od D:/Downloads` 
""")

    def extract(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(PyPDFBackend)],
        pages: Annotated[List[str] | None, typer.Option("--pages", "-pg",
                                                        help=_('Pages to extract (comma-separated list). Format "start-end".'),
                                                        )] = None,
        password: Annotated[str | None, PasswordOption()] = None,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pypdf_backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            pypdf_backend.extract(
                input_file=input_file,
                output_file=output_file,
                password=password,
                pages=parse_pdf_pages(pages),
                progress_callback=progress_mgr.update_progress
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem="_extracted")

        logger.info(f"{_('Extract pages')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfExtractTyperCommand",
]
