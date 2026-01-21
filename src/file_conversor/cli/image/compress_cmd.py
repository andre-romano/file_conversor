
# src\file_conversor\cli\image\compress_cmd.py

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules

from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption, QualityOption

from file_conversor.backend.image import CompressBackend

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation


from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageCompressTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = CompressBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # compress commands
        for ext in CompressBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="compress",
                    description="Compress",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -q 90"',
                    icon=str(icons_folder_path / 'compress.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.compress,
            help=f"""
    {_('Compress an image file (requires external libraries).')}

    {_('Outputs an image file with _compressed at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.jpg -q 85`

    - `file_conversor {group_name} {command_name} input_file.png -od D:/Downloads -o`
""")

    def compress(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(CompressBackend)],
        quality: Annotated[int, QualityOption()] = CONFIG.image_quality,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        compress_backend = CompressBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            logger.info(f"Processing '{output_file}' ... ")
            compress_backend.compress(
                input_file=input_file,
                output_file=output_file,
                quality=quality,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem="_compressed")

        logger.info(f"{_('Image compression')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageCompressTyperCommand",
]
