
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


class ImageCompressCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = ImageCompressCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # compress commands
        for mode in ImageCompressCommand.SupportedInFormats:
            ext = mode.value
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
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in ImageCompressCommand.SupportedInFormats)],
        quality: Annotated[int, QualityOption()] = CONFIG.image_quality,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            ImageCompressCommand.compress(
                input_files=input_files,
                quality=quality,
                output_dir=output_dir,
                progress_callback=task.update,
            )

        logger.info(f"{_('Image compression')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageCompressCLI",
]
