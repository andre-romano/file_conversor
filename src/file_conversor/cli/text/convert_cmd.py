
# src\file_conversor\cli\text\convert_cmd.py

from typing import Annotated, Any, Callable, List, Iterable
from pathlib import Path

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.backend import TextBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class TextConvertTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = TextBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for ext_in in TextBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext_in}", [
                WinContextCommand(
                    name=f"to_{ext_out}",
                    description=f"To {ext_out.upper()}",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" -f "{ext_out}" "%1""',
                    icon=str(icons_folder_path / f'{ext_out}.ico'),
                )
                for ext_out in TextBackend.SUPPORTED_OUT_FORMATS
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=_('Converts text file formats (json, xml, yaml, etc).'),
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} file1.json -f xml` 
""")

    def convert(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(TextBackend)],
        format: Annotated[str, FormatOption(TextBackend)],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        text_backend = TextBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            text_backend.convert(
                input_file=input_file,
                output_file=output_file,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_suffix=f".{format}")
        logger.info(f"{_('File conversion')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "TextConvertTyperCommand",
]
