
# src\file_conversor\cli\image\compress_cli.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    InputFilesArgument,
    OutputDirOption,
    QualityOption,
)
from file_conversor.command.image import ImageCompressCommand
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


class ImageCompressCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        # compress commands
        for ext_in in ImageCompressCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="compress",
                    description="Compress",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / 'compress.ico',
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
        input_files: Annotated[list[Path], InputFilesArgument(ImageCompressCommand.get_in_formats())],
        quality: Annotated[int, QualityOption()] = CONFIG.image_quality,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = ImageCompressCommand(
                input_files=input_files,
                quality=quality,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()

        logger.info(f"{_('Image compression')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageCompressCLI",
]
