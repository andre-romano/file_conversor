
# src\file_conversor\cli\pdf\rotate_cmd.py

from pathlib import Path
from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    InputFilesArgument,
    OutputDirOption,
    PasswordOption,
)
from file_conversor.command.pdf import PdfRotateCommand
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu
from file_conversor.utils.formatters import normalize_degree, parse_pdf_rotation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfRotateCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PdfRotateCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for mode in PdfRotateCommand.SupportedInFormats:
            ext = mode.value
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
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in PdfRotateCommand.SupportedInFormats)],
        rotation: Annotated[list[str], typer.Option("--rotation", "-r",
                                                    help=f'{_("List of pages to rotate. Format")} ``\"page:rotation\"`` {_("or")} ``\"start-end:rotation\"`` {_("or")} ``\"start-:rotation\"``. {_("Rotation can only be multiples of 90 degrees (e.g., -90, 0, 90, 180, 270).")}',
                                                    )],
        password: Annotated[str, PasswordOption()] = "",
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            try:
                PdfRotateCommand.rotate(
                    input_files=input_files,
                    rotation={
                        page: PdfRotateCommand.Rotation(normalize_degree(rotation_int))
                        for page, rotation_int in parse_pdf_rotation(rotation, PdfRotateCommand.len(input_files[0])).items()
                    },
                    password=password,
                    output_dir=output_dir,
                    progress_callback=task.update,
                )
            except ValueError as e:
                raise ValueError(
                    f"{_('Rotation values must be multiples of 90 degrees')}: {
                        ", ".join(str(mode.value) for mode in PdfRotateCommand.Rotation)
                    }."
                ) from e


__all__ = [
    "PdfRotateCLI",
]
