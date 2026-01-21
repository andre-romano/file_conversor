
# src\file_conversor\cli\image\render_cmd.py

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import DPIOption, FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.backend.image import PyMuSVGBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageRenderTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PyMuSVGBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # PyMuSVGBackend commands
        for ext in PyMuSVGBackend.SUPPORTED_IN_FORMATS:
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
        input_files: Annotated[List[Path], InputFilesArgument(PyMuSVGBackend)],
        format: Annotated[str, FormatOption(PyMuSVGBackend)],
        dpi: Annotated[int, DPIOption()] = CONFIG.image_dpi,
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pymusvg_backend = PyMuSVGBackend(verbose=STATE.loglevel.get().is_verbose())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            logger.info(f"Processing '{output_file}' ... ")
            pymusvg_backend.convert(
                input_file=input_file,
                output_file=output_file,
                dpi=dpi,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_suffix=f".{format}")

        logger.info(f"{_('Image render')}: [green bold]{_('SUCCESS')}[/]")


__all__ = [
    "ImageRenderTyperCommand",
]
