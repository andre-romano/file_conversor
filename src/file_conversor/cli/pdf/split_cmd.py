
# src\file_conversor\cli\pdf\split_cmd.py

from pathlib import Path
from typing import Annotated, Any, Callable, List, Iterable

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption, PasswordOption

from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfSplitTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PyPDFBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for ext in PyPDFBackend.SUPPORTED_IN_FORMATS:
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
        input_files: Annotated[List[Path], InputFilesArgument(PyPDFBackend)],
        password: Annotated[str | None, PasswordOption()] = None,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pypdf_backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            logger.info(f"Processing '{output_file}' ... ")
            pypdf_backend.split(
                input_file=input_file,
                output_file=output_file,
                password=password,
                progress_callback=progress_mgr.update_progress,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=True)  # avoid issues with existing files
        cmd_mgr.run(callback)
        logger.info(f"{_('Split pages')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfSplitTyperCommand",
]
