
# src\file_conversor\cli\pdf\repair_cmd.py

from pathlib import Path
from typing import Callable, Any, Annotated, List, Iterable

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption, PasswordOption

from file_conversor.backend.pdf import PikePDFBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfRepairTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PikePDFBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for ext in PikePDFBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="repair",
                    description="Repair",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / 'repair.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.repair,
            help=f"""
    {_('Attempt to repair a corrupted PDF file.')}        
    
    {_('Outputs a file with _repaired at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.pdf -od D:/Downloads` 
""")

    def repair(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(PikePDFBackend)],
        password: Annotated[str | None, PasswordOption()] = None,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pikepdf_backend = PikePDFBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            logger.info(f"Processing '{output_file}' ... ")
            pikepdf_backend.compress(
                # files
                input_file=input_file,
                output_file=output_file,

                # options
                decrypt_password=password,
                progress_callback=progress_mgr.update_progress
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem="_repaired")

        logger.info(f"{_('Repair PDF')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfRepairTyperCommand",
]
