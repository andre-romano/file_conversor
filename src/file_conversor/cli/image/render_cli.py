
# src\file_conversor\cli\image\render_cmd.py

from pathlib import Path
from typing import Annotated, override

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import (
    DPIOption,
    FormatOption,
    InputFilesArgument,
    OutputDirOption,
)
from file_conversor.command.image import ImageRenderCommand, ImageRenderOutFormats
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


class ImageRenderCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        for ext_in in ImageRenderCommand.get_in_formats():
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
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.render,
            help=_('Render an image vector file into a different format.'),
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name} input_file.svg -f png`

    - `file_conversor {group_name} {command_name} input_file.svg input_file2.svg -od D:/Downloads -f jpg --dpi 300`
""")

    def render(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(ImageRenderCommand.get_in_formats())],
        file_format: Annotated[ImageRenderOutFormats, FormatOption()],
        dpi: Annotated[int, DPIOption()] = CONFIG.image_dpi,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            command = ImageRenderCommand(
                input_files=input_files,
                file_format=file_format,
                dpi=dpi,
                output_dir=output_dir,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "ImageRenderCLI",
]
