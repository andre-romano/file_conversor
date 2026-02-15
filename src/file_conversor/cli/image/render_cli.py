
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
from file_conversor.command.image import ImageRenderCommand
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


class ImageRenderCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = ImageRenderCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # PyMuSVGBackend commands
        for mode in ImageRenderCommand.SupportedInFormats:
            ext = mode.value
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="to_jpg",
                    description="To JPG",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -f "jpg""',
                    icon=str(icons_folder_path / 'jpg.ico'),
                ),
                WinContextCommand(
                    name="to_png",
                    description="To PNG",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1" -f "png""',
                    icon=str(icons_folder_path / 'png.ico'),
                ),
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
        input_files: Annotated[list[Path], InputFilesArgument(mode.value for mode in ImageRenderCommand.SupportedInFormats)],
        file_format: Annotated[ImageRenderCommand.SupportedOutFormats, FormatOption()],
        dpi: Annotated[int, DPIOption()] = CONFIG.image_dpi,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Processing files:"))
            ImageRenderCommand.render(
                input_files=input_files,
                file_format=file_format,
                dpi=dpi,
                output_dir=output_dir,
                progress_callback=task.update,
            )


__all__ = [
    "ImageRenderCLI",
]
