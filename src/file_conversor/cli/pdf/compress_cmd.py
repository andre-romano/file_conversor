
# src\file_conversor\cli\pdf\compress_cmd.py

import tempfile
import typer

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption

from file_conversor.backend.pdf import PikePDFBackend, GhostscriptBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils.formatters import get_output_file

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfCompressTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = {
        *PikePDFBackend.EXTERNAL_DEPENDENCIES,
        *GhostscriptBackend.EXTERNAL_DEPENDENCIES,
    }

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for ext in GhostscriptBackend.SUPPORTED_IN_FORMATS:
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
        input_files: Annotated[List[Path], InputFilesArgument(GhostscriptBackend)],
        compression: Annotated[GhostscriptBackend.Compression, typer.Option("--compression", "-c",
                                                                            help=f"{_('Compression level (high compression = low quality). Valid values are')} {', '.join(mode.value for mode in GhostscriptBackend.Compression)}. {_('Defaults to')} {CONFIG.pdf_compression}.",
                                                                            )] = GhostscriptBackend.Compression(CONFIG.pdf_compression),
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pikepdf_backend = PikePDFBackend(
            verbose=STATE.loglevel.get().is_verbose(),
        )
        gs_backend = GhostscriptBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            with tempfile.TemporaryDirectory() as temp_dir:
                gs_out = Path(temp_dir) / get_output_file(input_file, stem="_gs")
                gs_backend.compress(
                    input_file=input_file,
                    output_file=gs_out,
                    compression_level=compression,
                    progress_callback=progress_mgr.update_progress
                )
                progress_mgr.complete_step()

                pikepdf_backend.compress(
                    # files
                    input_file=gs_out,
                    output_file=output_file,
                    progress_callback=progress_mgr.update_progress
                )
                progress_mgr.complete_step()
                logger.info(f"Processing '{output_file}' ... OK")

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, steps=2, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem="_compressed")

        logger.info(f"{_('File compression')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "PdfCompressTyperCommand",
]
