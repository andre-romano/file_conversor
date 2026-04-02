
# src\file_conversor\cli\doc\convert_cli.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
)
from file_conversor.command.doc import DocConvertCommand, DocConvertOutFormats
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


class DocConvertCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        # WordBackend commands
        for ext_in in DocConvertCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name=f"to_{ext_out}",
                    description=f"To {ext_out.upper()}",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-f", ext_out],
                    icon=icons_folder / f"{ext_out}.ico",
                )
                for ext_out in DocConvertCommand.get_out_formats()
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=_('Convert document files into other formats (requires LibreOffice).'),
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.odt -f doc`

    - `file_conversor {group_name} {command_name} input_file.docx -f pdf`

    - `file_conversor {group_name} {command_name} input_file.pdf -f docx`
""")

    def convert(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(DocConvertCommand.get_in_formats())],
        file_format: Annotated[DocConvertOutFormats, FormatOption()],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        """Convert document files into other formats."""
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = DocConvertCommand(
                input_files=input_files,
                file_format=file_format,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "DocConvertCLI",
]
