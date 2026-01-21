
# src\file_conversor\cli\doc\convert_cmd.py

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich
from file_conversor.cli._utils.typer import FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.backend import LibreofficeWriterBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils.formatters import format_in_out_files_tuple

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class DocConvertCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = LibreofficeWriterBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # WordBackend commands
        icons_folder_path = Environment.get_icons_folder()
        for ext in LibreofficeWriterBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name=f"to_{ext}",
                    description=f"To {ext.upper()}",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -f "{ext}""',
                    icon=str(icons_folder_path / f"{ext}.ico"),
                )
                for ext in LibreofficeWriterBackend.SUPPORTED_OUT_FORMATS
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
        input_files: Annotated[List[Path], InputFilesArgument(LibreofficeWriterBackend.SUPPORTED_IN_FORMATS)],
        format: Annotated[str, FormatOption(LibreofficeWriterBackend.SUPPORTED_OUT_FORMATS)],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):

        files = [
            LibreofficeWriterBackend.FilesDataModel(
                input_file=input,
                output_file=output,
            )
            for input, output in format_in_out_files_tuple(
                input_files=input_files,
                output_dir=output_dir,
                file_format=format,
                overwrite_output=STATE.overwrite_output.enabled,
            )
        ]

        backend = LibreofficeWriterBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        with ProgressManagerRich(len(input_files)) as progress_mgr:
            logger.info(f"[bold]{_('Converting files')}[/] ...")
            # Perform conversion
            backend.convert(
                files=files,
                file_processed_callback=lambda _: progress_mgr.complete_step()
            )

        logger.info(f"{_('File conversion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "DocConvertCommand",
]
