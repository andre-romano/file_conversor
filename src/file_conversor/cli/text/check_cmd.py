
# src\file_conversor\cli\text\check_cmd.py

from pathlib import Path
from typing import Annotated, Any, Callable, List, Iterable

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument

from file_conversor.backend import TextBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class TextCheckTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = TextBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for ext in TextBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="check",
                    description="Check",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / 'check.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.check,
            help=_('Checks a text file schema compliance (json, xml, yaml, etc).'),
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} file.json` 

    - `file_conversor {group_name} {command_name} file1.json file2.yaml` 
""")

    def check(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(TextBackend)],
    ):
        text_backend = TextBackend(verbose=STATE.loglevel.get().is_verbose())
        logger.info(f"{_('Checking files')} ...")

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            text_backend.check(
                input_file=input_file,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=Path(), overwrite=True)  # overwrite is True because no output files are generated
        cmd_mgr.run(callback)

        logger.info(f"{_('Check')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "TextCheckTyperCommand",
]
