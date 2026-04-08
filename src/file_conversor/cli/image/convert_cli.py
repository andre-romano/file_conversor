
# src\file_conversor\cli\image\convert_cli.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
    QualityOption,
)
from file_conversor.command.image import ImageConvertCommand, ImageConvertOutFormats
from file_conversor.config import (
    CONFIG,
    LOG,
    STATE,
    get_translation,
)
from file_conversor.system import ContextMenu, ContextMenuItem


_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageConvertCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        # Pillow commands
        for ext_in in ImageConvertCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name=f"to_{ext_out}",
                    description=f"To {ext_out.upper()}",
                    args=[self.GROUP_NAME, self.COMMAND_NAME, "-f", ext_out],
                    icon=icons_folder / f'{ext_out}.ico',
                )
                for ext_out in ["jpg", "png"]
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        """Config set command class."""
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.convert,
            help=_('Convert a image file to a different format.'),
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.webp -f jpg --quality 85`

    - `file_conversor {group_name} {command_name} input_file.bmp -f png -od D:/Downloads`
""")

    def convert(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(ImageConvertCommand.get_in_formats())],
        file_format: Annotated[ImageConvertOutFormats, FormatOption()],
        quality: Annotated[int, QualityOption()] = CONFIG.image_quality,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = ImageConvertCommand(
                input_files=input_files,
                file_format=file_format,
                quality=quality,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "ImageConvertCLI",
]
