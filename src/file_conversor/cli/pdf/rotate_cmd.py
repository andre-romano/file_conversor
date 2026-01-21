
# src\file_conversor\cli\pdf\rotate_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption, PasswordOption

from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.formatters import parse_pdf_rotation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfRotateTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PyPDFBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for ext in PyPDFBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="rotate_anticlock_90",
                    description="Rotate Left",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -r "1-:-90""',
                    icon=str(icons_folder_path / "rotate_left.ico"),
                ),
                WinContextCommand(
                    name="rotate_clock_90",
                    description="Rotate Right",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -r "1-:90""',
                    icon=str(icons_folder_path / "rotate_right.ico"),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.rotate,
            help=f"""
    {_('Rotate PDF pages (clockwise or anti-clockwise).')}
    
    {_('Outputs a file with _rotated at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 



    *{_('Rotate page 1 by 180 degress')}*:

    - `file_conversor {group_name} {command_name} input_file.pdf -o output_file.pdf -r "1:180"` 



    *{_('Rotate page 5-7 by 90 degress, 9 by -90 degrees, 10-15 by 180 degrees')}*:

    - `file_conversor {group_name} {command_name} input_file.pdf -r "5-7:90" -r "9:-90" -r "10-15:180"`
""")

    def rotate(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(PyPDFBackend)],
        rotation: Annotated[List[str], typer.Option("--rotation", "-r",
                                                    help=_("List of pages to rotate. Format ``\"page:rotation\"`` or ``\"start-end:rotation\"`` or ``\"start-:rotation\"`` ..."),
                                                    )],
        password: Annotated[str | None, PasswordOption()] = None,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pypdf_backend = PyPDFBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            pypdf_backend.rotate(
                input_file=input_file,
                output_file=output_file,
                decrypt_password=password,
                rotations=parse_pdf_rotation(rotation, pypdf_backend.len(input_file)),
                progress_callback=progress_mgr.update_progress,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem="_rotated")
        logger.info(f"{_('Rotate pages')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PdfRotateTyperCommand",
]
