
# src\file_conversor\cli\pdf\compress_cmd.py

from pathlib import Path
from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption
from file_conversor.command.pdf import PdfCompressCommand
from file_conversor.config import (
    Configuration,
    Environment,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfCompressCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PdfCompressCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for mode in PdfCompressCommand.SupportedInFormats:
            ext = mode.value
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
    {_('Reduce the file size of a PDF document (requires Ghostscript external library).')}
    
    {_('Outputs a file with _compressed at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.pdf -od D:/Downloads`

    - `file_conversor {group_name} {command_name} input_file.pdf -c high`

    - `file_conversor {group_name} {command_name} input_file.pdf -o`
""")

    def compress(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in PdfCompressCommand.SupportedInFormats)],
        compression: Annotated[PdfCompressCommand.Compression, typer.Option("--compression", "-c",
                                                                            help=f"{_('Compression level (high compression = low quality). Valid values are')} {', '.join(mode.value for mode in PdfCompressCommand.Compression)}. {_('Defaults to')} {CONFIG.pdf_compression}.",
                                                                            )] = PdfCompressCommand.Compression(CONFIG.pdf_compression),
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            PdfCompressCommand.compress(
                input_files=input_files,
                compression=compression,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "PdfCompressCLI",
]
