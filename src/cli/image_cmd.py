
# src\cli\image_cmd.py

import typer

from typing import Annotated

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.console import Group

# user-provided modules
from backend import PillowBackend

from config import Configuration, State
from config.locale import get_translation

from utils import File
from utils.rich import get_progress_bar
from utils.validators import check_file_format, check_axis

# get app config
_ = get_translation()
CONFIG = Configuration.get_instance()
STATE = State.get_instance()

image_cmd = typer.Typer()


# image info
@image_cmd.command(
    help=f"""
        {_('Get EXIF information about a image file.')}

        {_('This command retrieves metadata and other information about the image file')}:
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor image info filename.webp`

        - `file_conversor image info other_filename.jpg`
    """)
def info(
    filename: Annotated[str, typer.Argument(
        help=_("File path"),
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],
):

    formatted = []
    metadata: PillowBackend.Exif
    with get_progress_bar() as progress:
        task = progress.add_task(f"{_('Parsing file metadata')} ...", total=None)

        pillow_backend = PillowBackend(verbose=STATE['verbose'])
        metadata = pillow_backend.info(filename)
        progress.update(task, total=100, completed=100)

    # 📁 Informações gerais do arquivo
    formatted.append(f"  - {_('Name')}: {filename}")
    formatted.append(f"  - {_('Format')}: {File(filename).get_extension().upper()}")
    if metadata:
        for tag, value in metadata.items():
            tag_name = PillowBackend.Exif_TAGS.get(tag, f"{tag}")
            formatted.append(f"  - {tag_name}: {value}")

    # Agrupar e exibir tudo com Rich
    group = Group(*formatted)
    print(Panel(group, title=f"🧾 {_('File Analysis')}", border_style="blue"))


# image convert
@image_cmd.command(
    help=f"""
        {_('Convert a image file to a different format.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor image convert input_file.webp output_file.jpg --quality 85`

        - `file_conversor image convert input_file.bmp output_file.png`
    """)
def convert(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file path')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    output_file: Annotated[str, typer.Argument(
        help=f"{_('Output file path')} ({', '.join(PillowBackend.SUPPORTED_OUT_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_OUT_FORMATS),
    )],

    quality: Annotated[int, typer.Option("--quality", "-q",
                                         help=_("Image quality. Valid values are between 1-100."),
                                         min=1, max=100,
                                         )] = CONFIG["image-quality"],
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])
    # display current progress
    with get_progress_bar() as progress:
        task = progress.add_task(f"{_('Processing file')} ...", total=None)
        pillow_backend.convert(
            input_file=input_file,
            output_file=output_file,
            quality=quality,
        )
        progress.update(task, total=100, completed=100)
    print(f"--------------------------------")
    print(f"{_('Image convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
    print(f"--------------------------------")


# image rotate
@image_cmd.command(
    help=f"""
        {_('Rotate a image file (clockwise or anti-clockwise).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor pdf rotate input_file.jpg output_file.jpg 90` 
        
        - `file_conversor pdf rotate input_file.jpg output_file.jpg -180` 
    """)
def rotate(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file path')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    output_file: Annotated[str, typer.Argument(
        help=f"{_('Output file path')} ({', '.join(PillowBackend.SUPPORTED_OUT_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_OUT_FORMATS),
    )],

    rotation: Annotated[int, typer.Option("--rotation", "-r",
                                          help=_("Rotation in degrees. Valid values are between -360 (anti-clockwise rotation) and 360 (clockwise rotation)."),
                                          min=-360, max=360,
                                          )],
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])
    # display current progress
    with get_progress_bar() as progress:
        task = progress.add_task(f"{_('Processing file')} ...", total=None)
        pillow_backend.rotate(
            input_file=input_file,
            output_file=output_file,
            rotate=rotation,
        )
        progress.update(task, total=100, completed=100)
    print(f"--------------------------------")
    print(f"{_('Image rotation')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
    print(f"--------------------------------")


# image mirror
@image_cmd.command(
    help=f"""
        {_('Mirror an image file (vertically or horizontally).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor pdf mirror input_file.jpg output_file.jpg -a x` 
        
        - `file_conversor pdf mirror input_file.jpg output_file.jpg -a y` 
    """)
def mirror(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file path')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    output_file: Annotated[str, typer.Argument(
        help=f"{_('Output file path')} ({', '.join(PillowBackend.SUPPORTED_OUT_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_OUT_FORMATS),
    )],

    axis: Annotated[int, typer.Option("--axis", "-a",
                                      help=_("Axis. Valid values are 'x' (mirror horizontally) or 'y' (flip vertically)."),
                                      callback=check_axis,
                                      )],
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])
    # display current progress
    with get_progress_bar() as progress:
        task = progress.add_task(f"{_('Processing file')} ...", total=None)
        pillow_backend.mirror(
            input_file=input_file,
            output_file=output_file,
            x_y=True if axis == "x" else False,
        )
        progress.update(task, total=100, completed=100)
    print(f"--------------------------------")
    print(f"{_('Image mirroring')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
    print(f"--------------------------------")
