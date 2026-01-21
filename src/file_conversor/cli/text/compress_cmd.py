
# src\file_conversor\cli\text\compress_cmd.py

from typing import Annotated, Any, Callable, List, Iterable
from pathlib import Path

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption

from file_conversor.backend import TextBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class TextCompressTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = TextBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for ext in TextBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="compress",
                    description="Compress",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / 'compress.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.compress,
            help=f"""
    {_('Compress / minify text file formats (json, xml, yaml, etc).')}        
    
    {_('Outputs a file with .min at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} file1.json` 
""")

    def compress(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(TextBackend)],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        text_backend = TextBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            text_backend.minify(
                input_file=input_file,
                output_file=output_file,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem=f"_compressed")
        logger.info(f"{_('Compression')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "TextCompressTyperCommand",
]
