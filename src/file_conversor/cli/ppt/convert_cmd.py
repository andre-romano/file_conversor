
# src\file_conversor\cli\ppt\convert_cmd.py

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.backend import LibreofficeImpressBackend

from file_conversor.config import Configuration, Environment, Log, State, get_translation

from file_conversor.utils.formatters import format_in_out_files_tuple

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PptConvertTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = LibreofficeImpressBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # WordBackend commands
        for ext in LibreofficeImpressBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name=f"to_{ext}",
                    description=f"To {ext.upper()}",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f "{ext}" "%1""',
                    icon=str(icons_folder_path / f"{ext}.ico"),
                )
                for ext in LibreofficeImpressBackend.SUPPORTED_OUT_FORMATS
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=f"""
    {_('Convert presentation files into other formats (requires LibreOffice).')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.odp -o output_file.ppt`

    - `file_conversor {group_name} {command_name} input_file.pptx -o output_file.pdf`
""")

    def convert(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(LibreofficeImpressBackend)],
        format: Annotated[str, FormatOption(LibreofficeImpressBackend)],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        files = [
            LibreofficeImpressBackend.FilesDataModel(
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

        backend = LibreofficeImpressBackend(
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
    "PptConvertTyperCommand",
]
