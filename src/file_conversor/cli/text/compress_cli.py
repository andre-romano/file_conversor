
# src\file_conversor\cli\text\compress_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption
from file_conversor.command.text import TextCompressCommand
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


class TextCompressCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        for ext_in in TextCompressCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="compress",
                    description="Compress",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / 'compress.ico',
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
        input_files: Annotated[list[Path], InputFilesArgument(TextCompressCommand.get_in_formats())],
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = TextCompressCommand(
                input_files=input_files,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "TextCompressCLI",
]
