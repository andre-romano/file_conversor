
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
from file_conversor.command.pdf.rotate_cmd import PdfRotateRotation
from file_conversor.config import (
    Configuration,
    Log,
    State,
    get_translation,
)
from file_conversor.system import ContextMenu, ContextMenuItem
from file_conversor.utils.formatters import normalize_degree, parse_pdf_rotation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfRotateCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        for ext_in in PdfRotateCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="rotate_anticlock_90",
                    description="Rotate Left",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-r", "1-:-90"],
                    icon=icons_folder / "rotate_left.ico",
                ),
                ContextMenuItem(
                    name="rotate_clock_90",
                    description="Rotate Right",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-r", "1-:90"],
                    icon=icons_folder / "rotate_right.ico",
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
        input_files: Annotated[list[Path], InputFilesArgument(PdfRotateCommand.get_in_formats())],
        rotation: Annotated[list[str], typer.Option("--rotation", "-r",
                                                    help=f'{_("List of pages to rotate. Format")} ``\"page:rotation\"`` {_("or")} ``\"start-end:rotation\"`` {_("or")} ``\"start-:rotation\"``. {_("Rotation can only be multiples of 90 degrees (e.g., -90, 0, 90, 180, 270).")}',
                                                    )],
        password: Annotated[str, PasswordOption()] = "",
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            try:
                command = PdfRotateCommand(
                    input_files=input_files,
                    rotation={
                        page: PdfRotateRotation(normalize_degree(rotation_int))
                        for page, rotation_int in parse_pdf_rotation(rotation, PdfRotateCommand.len(input_files[0])).items()
                    },
                    password=password,
                    output_dir=output_dir,
                    progress_callback=task.update,
                )
                command.execute()
            except ValueError as e:
                raise ValueError(
                    f"{_('Rotation values must be multiples of 90 degrees')}: {
                        ", ".join(str(mode.value) for mode in PdfRotateRotation)
                    }."
                ) from e


__all__ = [
    "PdfRotateCLI",
]
