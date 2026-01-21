
# src\file_conversor\cli\ebook\convert_cmd.py

from typing import Annotated, Any, Callable, Iterable, List
from pathlib import Path

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.backend import CalibreBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class EbookConvertCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = CalibreBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        # FFMPEG commands
        icons_folder_path = Environment.get_icons_folder()
        for ext in CalibreBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name=f"to_{ext}",
                    description=f"To {ext.upper()}",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -f "{ext}""',
                    icon=str(icons_folder_path / f"{ext}.ico"),
                )
                for ext in CalibreBackend.SUPPORTED_OUT_FORMATS
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=_('Convert an ebook file to another ebook format or PDF (requires Calibre).'),
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.epub -f pdf -od output_dir/`
    - `file_conversor {group_name} {command_name} input_file.mobi -f epub`
""")

    def convert(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(CalibreBackend.SUPPORTED_IN_FORMATS)],
        format: Annotated[str, FormatOption(CalibreBackend.SUPPORTED_OUT_FORMATS)],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        """Execute ebook conversion command."""
        calibre_backend = CalibreBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            calibre_backend.convert(
                input_file=input_file,
                output_file=output_file,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_suffix=f".{format}")

        logger.info(f"{_('File conversion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "EbookConvertCommand",
]
