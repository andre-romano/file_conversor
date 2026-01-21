
# src\file_conversor\cli\pdf\merge_cmd.py

from pathlib import Path
from typing import Annotated, Any, Callable, List, Iterable

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputFileOption, PasswordOption

from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextMenu
from file_conversor.utils.formatters import get_output_file
from file_conversor.utils.validators import check_path_exists

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfMergeTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PyPDFBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # no context menu for this command

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.merge,
            help=f"""
    {_('Merge (join) input PDFs into a single PDF file.')}
    
    {_('Outputs a file with _merged at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 



    *{_('Merge files "input_file1.pdf" and "input_file2.pdf" into "output_file.pdf"')}*:

    - `file_conversor {group_name} {command_name} "input_file1.pdf" "input_file2.pdf" -of output_file.pdf` 



    *{_('Merge protected PDFs "input_file1.pdf" and "input_file2.pdf" with password "unlock_password"')}*:

    - `file_conversor {group_name} {command_name} "input_file1.pdf" "input_file2.pdf" -p "unlock_password" -of output_file.pdf` 
""")

    def merge(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(PyPDFBackend)],
        password: Annotated[str | None, PasswordOption()] = None,
        output_file: Annotated[Path | None, OutputFileOption(PyPDFBackend)] = None,
    ):
        output_file = output_file if output_file else Path() / get_output_file(input_files[0], stem="_merged")
        if not STATE.overwrite_output.enabled:
            check_path_exists(output_file, exists=False)

        pypdf_backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())
        with ProgressManagerRich() as progress_mgr:
            logger.info(f"Processing '{output_file}' ...")
            pypdf_backend.merge(
                # files
                input_files=input_files,
                output_file=output_file,
                password=password,
                progress_callback=progress_mgr.update_progress
            )
            progress_mgr.complete_step()

        logger.info(f"{_('Merge pages')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfMergeTyperCommand",
]
