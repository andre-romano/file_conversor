
# src\file_conversor\cli\multimedia\image_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, Iterable, List

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption

from file_conversor.backend.image import PillowBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils.formatters import parse_image_resize_scale
from file_conversor.utils.validators import check_positive_integer

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ImageResizeTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        # Pillow commands
        for ext in PillowBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="resize",
                    description="Resize",
                    command=f'cmd.exe /k "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / "resize.ico"),
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
        input_files: Annotated[List[Path], InputFilesArgument(PillowBackend)],
        scale: Annotated[float | None, typer.Option("--scale", "-s",
                                                    help=f"{_("Scale image proportion. Valid values start at 0.1. Defaults to")} None (use width to scale image).",
                                                    callback=lambda x: check_positive_integer(x),
                                                    )] = None,

        width: Annotated[int | None, typer.Option("--width", "-w",
                                                  help=f"{_("Width in pixels (height is calculated based on width to keep image proportions). Defaults to")} None ({_('use scale to resize image')}).",
                                                  callback=lambda x: check_positive_integer(x),
                                                  )] = None,

        resampling: Annotated[PillowBackend.ResamplingOption, typer.Option("--resampling", "-r",
                                                                           help=f'{_("Resampling algorithm. Valid values are")} {", ".join(mode.value for mode in PillowBackend.ResamplingOption)}. {_("Defaults to")} {CONFIG.image_resampling}.',
                                                                           )] = PillowBackend.ResamplingOption(CONFIG.image_resampling),
        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        pillow_backend = PillowBackend(verbose=STATE.loglevel.get().is_verbose())

        scale = parse_image_resize_scale(scale, width, quiet=STATE.loglevel.get().is_quiet())

        def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManagerRich):
            logger.info(f"Processing '{output_file}' ... ")
            pillow_backend.resize(
                input_file=input_file,
                output_file=output_file,
                scale=scale,
                width=width,
                resampling=resampling,
            )
            progress_mgr.complete_step()

        cmd_mgr = CommandManagerRich(input_files, output_dir=output_dir, overwrite=STATE.overwrite_output.enabled)
        cmd_mgr.run(callback, out_stem="_resized")

        logger.info(f"{_('Image resize')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "ImageResizeTyperCommand",
]
