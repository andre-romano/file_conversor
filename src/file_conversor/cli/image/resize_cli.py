
# src\file_conversor\cli\image\resize_cli.py

from pathlib import Path
from typing import Annotated, override

import typer

# CLI
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption

# COMMAND
from file_conversor.command.image import ImageResizeCommand, ImageResizeResamplingOption
from file_conversor.config import CONFIG, LOG, STATE, get_translation
from file_conversor.system import ContextMenu, ContextMenuItem
from file_conversor.utils.validators import prompt_retry_on_exception


_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageResizeCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        # Pillow commands
        for ext_in in ImageResizeCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="resize",
                    description="Resize",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / "resize.ico",
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.resize,
            help=f"""
    {_('Resize an image file.')}

    {_('Outputs an image file with _resized at the end.')}
""",
            epilog=f"""
    **{_('Examples')}:**



    *{_('Double the image size')}*:

    - `file_conversor {group_name} {command_name} input_file.jpg -s 2.0`



    *{_('Set the image width to 1024px')}*:

    - `file_conversor {group_name} {command_name} input_file.jpg -od D:/Downloads -w 1024`
""")

    def resize(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(ImageResizeCommand.get_in_formats())],
        scale: Annotated[float | None, typer.Option("--scale", "-s",
                                                    help=f"{_("Scale image proportion. Valid values start at 0.1.")}",
                                                    min=0.1,
                                                    )] = None,

        width: Annotated[int | None, typer.Option("--width", "-w",
                                                  help=f"{_("Width in pixels (height is calculated based on width to keep image proportions).")}",
                                                  min=1,
                                                  )] = None,

        resampling: Annotated[ImageResizeResamplingOption, typer.Option("--resampling", "-r",
                                                                        help=f'{_("Resampling algorithm.")}',
                                                                        )] = ImageResizeResamplingOption(CONFIG.image_resampling),
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        if scale is None and width is None:
            if STATE.loglevel.get().is_quiet():
                raise RuntimeError(f"{_('Scale and width not provided')}")
            scale = prompt_retry_on_exception(
                f"{_('Output image scale (e.g., 1.5)')}",
                type=float,
                callback=lambda x: x > 0.0
            )

        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = ImageResizeCommand(
                input_files=input_files,
                scale=scale,
                width=width,
                resampling=resampling,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "ImageResizeCLI",
]
