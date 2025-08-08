
# src\file_conversor\cli\image_cmd.py

import typer

from pathlib import Path
from typing import Annotated, List

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.console import Group

# user-provided modules
from file_conversor.backend import PillowBackend, Img2PDFBackend

from file_conversor.config import Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import File
from file_conversor.utils.rich import get_progress_bar
from file_conversor.utils.validators import check_file_format, check_is_bool_or_none, check_valid_options

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

image_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = State.get_icons_folder()
    # IMG2PDF commands
    for ext in Img2PDFBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_pdf",
                description="To PDF",
                command=f'{State.get_executable()} image to-pdf "%1"',
                icon=str(icons_folder_path / "pdf.ico"),
            ),
        ])
    # Pillow commands
    for ext in PillowBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="info",
                description="Get Info",
                command=f'cmd /k "{State.get_executable()} image info "%1""',
                icon=str(icons_folder_path / "info.ico"),
            ),
            WinContextCommand(
                name="to_jpg",
                description="To JPG",
                command=f'{State.get_executable()} image convert "%1" -o "%1.jpg" -q 95',
                icon=str(icons_folder_path / 'jpg.ico'),
            ),
            WinContextCommand(
                name="to_png",
                description="To PNG",
                command=f'{State.get_executable()} image convert "%1" -o "%1.png" -q 95',
                icon=str(icons_folder_path / 'png.ico'),
            ),
            WinContextCommand(
                name="to_webp",
                description="To WEBP",
                command=f'{State.get_executable()} image convert "%1" -o "%1.webp" -q 95',
                icon=str(icons_folder_path / 'webp.ico'),
            ),
            WinContextCommand(
                name="rotate_anticlock_90",
                description="Rotate Left",
                command=f'{State.get_executable()} image rotate "%1" -r -90',
                icon=str(icons_folder_path / "rotate_left.ico"),
            ),
            WinContextCommand(
                name="rotate_clock_90",
                description="Rotate Right",
                command=f'{State.get_executable()} image rotate "%1" -r 90',
                icon=str(icons_folder_path / "rotate_right.ico"),
            ),
            WinContextCommand(
                name="mirror_x",
                description="Mirror X axis",
                command=f'{State.get_executable()} image mirror "%1" -a x',
                icon=str(icons_folder_path / "left_right.ico"),
            ),
            WinContextCommand(
                name="mirror_y",
                description="Mirror Y axis",
                command=f'{State.get_executable()} image mirror "%1" -a y',
                icon=str(icons_folder_path / "up_down.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


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
        help=f"{_('File')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
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


# image to-pdf
@image_cmd.command(
    help=f"""
        {_('Convert a list of image files to one PDF file, one image per page.')}

        Fit = {_('Valid only if ``--page-size`` is defined. Otherwise, PDF size = figure size.')}

        - 'into': {_('Figure adjusted to fit in PDF size')}.

        - 'fill': {_('Figure adjusted to fit in PDF size')}, {_('without any empty borders (cut figure if needed)')}.
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor image to-pdf input_file.jpg -o output_file.pdf --dpi 96`

        - `file_conversor image to-pdf input_file1.bmp input_file2.png -o output_file.pdf`

        - `file_conversor image to-pdf input_file.jpg -o output_file.pdf -ps a4_landscape`

        - `file_conversor image to-pdf input_file1.bmp input_file2.png -o output_file.pdf --page-size (21.00,29.70)`
    """)
def to_pdf(
    input_files: Annotated[List[str], typer.Argument(help=f"{_('Input files')} ({', '.join(Img2PDFBackend.SUPPORTED_IN_FORMATS)})",
                                                     callback=lambda x: check_file_format(x, Img2PDFBackend.SUPPORTED_IN_FORMATS, exists=True),
                                                     )],

    output_file: Annotated[str | None, typer.Option("--output", "-o",
                                                    help=f"{_('Output file')} ({', '.join(Img2PDFBackend.SUPPORTED_OUT_FORMATS)}). {_('Defaults to None')} ({_('use the same 1st input file as output name')}).",
                                                    callback=lambda x: check_file_format(x, Img2PDFBackend.SUPPORTED_OUT_FORMATS),
                                                    )] = None,

    dpi: Annotated[int, typer.Option("--dpi", "-d",
                                     help=_("Image quality in dots per inch (DPI). Valid values are between 40-3600."),
                                     min=40, max=3600,
                                     )] = CONFIG["image-dpi"],

    fit: Annotated[str, typer.Option("--fit", "-f",
                                     help=_("Image fit. Valid only if ``--page-size`` is defined. Valid values are 'into', or 'fill'. Defaults to 'into'. "),
                                     callback=lambda x: check_valid_options(x.lower(), ['into', 'fill']),
                                     )] = CONFIG["image-fit"],

    page_size: Annotated[str | None, typer.Option("--page-size", "-ps",
                                                  help=_("Page size. Format '(width, height)'. Other valid values are: 'a4', 'a4_landscape'. Defaults to None (PDF size = image size)."),
                                                  callback=lambda x: check_valid_options(x.lower() if x else None, [None, 'a4', 'a4_landscape']),
                                                  )] = CONFIG["image-page-size"],

    set_metadata: Annotated[bool, typer.Option("--set-metadata", "-sm",
                                               help=_("Set PDF metadata. Defaults to True (set creator, producer, modification date, etc)."),
                                               callback=check_is_bool_or_none,
                                               is_flag=True,
                                               )] = CONFIG["image-set-metadata"],
):
    img2pdf_backend = Img2PDFBackend(verbose=STATE['verbose'])
    # display current progress
    with get_progress_bar() as progress:
        task = progress.add_task(f"{_('Processing file')} '{output_file}':", total=None)

        # parse user input
        image_fit: Img2PDFBackend.FIT_MODE
        if fit == 'into':
            image_fit = Img2PDFBackend.FIT_INTO
        elif fit == 'fill':
            image_fit = Img2PDFBackend.FIT_FILL

        page_sz: tuple | None
        if page_size is None:
            page_sz = Img2PDFBackend.LAYOUT_NONE
        elif page_size == 'a4':
            page_sz = Img2PDFBackend.LAYOUT_A4_PORTRAIT_CM
        elif page_size == 'a4_landscape':
            page_sz = Img2PDFBackend.LAYOUT_A4_LANDSCAPE_CM
        else:
            page_sz = tuple(page_size)

        img2pdf_backend.to_pdf(
            input_files=input_files,
            output_file=output_file if output_file else f"{input_files[0].replace(".pdf", "")}.pdf",
            dpi=dpi,
            image_fit=image_fit,
            page_size=page_sz,
            include_metadata=set_metadata,
        )
        progress.update(task, total=100, completed=100)
    logger.info(f"{_('PDF generation')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


# image convert
@image_cmd.command(
    help=f"""
        {_('Convert a image file to a different format.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor image convert input_file.webp -o output_file.jpg --quality 85`

        - `file_conversor image convert input_file.bmp -o output_file.png`
    """)
def convert(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    output_file: Annotated[str, typer.Option("--output", "-o",
                                             help=f"{_('Output file')} ({', '.join(PillowBackend.SUPPORTED_OUT_FORMATS)})",
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
        task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None)
        pillow_backend.convert(
            input_file=input_file,
            output_file=output_file,
            quality=quality,
        )
        progress.update(task, total=100, completed=100)
    logger.info(f"{_('Image convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


# image rotate
@image_cmd.command(
    help=f"""
        {_('Rotate a image file (clockwise or anti-clockwise).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor pdf rotate input_file.jpg -o output_file.jpg -r 90` 
        
        - `file_conversor pdf rotate input_file.jpg -o output_file.jpg -r -180` 
    """)
def rotate(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    rotation: Annotated[int, typer.Option("--rotation", "-r",
                                          help=_("Rotation in degrees. Valid values are between -360 (anti-clockwise rotation) and 360 (clockwise rotation)."),
                                          min=-360, max=360,
                                          )],
    output_file: Annotated[str | None, typer.Option("--output", "-o",
                                                    help=f"{_('Output file')} ({', '.join(PillowBackend.SUPPORTED_OUT_FORMATS)}). {_('Defaults to None')} ({_('use the same input file as output name')}, {_('with _rotated at the end)')}",
                                                    callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_OUT_FORMATS),
                                                    )] = None,
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])
    # display current progress
    with get_progress_bar() as progress:
        in_file = File(input_file)

        task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None)
        pillow_backend.rotate(
            input_file=input_file,
            output_file=output_file if output_file else f"{in_file.get_filename()}_rotated.{in_file.get_extension()}",
            rotate=rotation,
        )
        progress.update(task, total=100, completed=100)
    logger.info(f"{_('Image rotation')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


# image mirror
@image_cmd.command(
    help=f"""
        {_('Mirror an image file (vertically or horizontally).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor pdf mirror input_file.jpg -o output_file.jpg -a x` 
        
        - `file_conversor pdf mirror input_file.jpg -o output_file.jpg -a y` 
    """)
def mirror(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    axis: Annotated[str, typer.Option("--axis", "-a",
                                      help=_("Axis. Valid values are 'x' (mirror horizontally) or 'y' (flip vertically)."),
                                      callback=lambda x: check_valid_options(x, valid_options=['x', 'y']),
                                      )],
    output_file: Annotated[str | None, typer.Option("--output", "-o",
                                                    help=f"{_('Output file')} ({', '.join(PillowBackend.SUPPORTED_OUT_FORMATS)}). {_('Defaults to None')} ({_('use the same input file as output name')}, {_('with _mirrored at the end)')}",
                                                    callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_OUT_FORMATS),
                                                    )] = None,
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])
    # display current progress
    with get_progress_bar() as progress:
        in_file = File(input_file)

        task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None)
        pillow_backend.mirror(
            input_file=input_file,
            output_file=output_file if output_file else f"{in_file.get_filename()}_mirrored.{in_file.get_extension()}",
            x_y=True if axis == "x" else False,
        )
        progress.update(task, total=100, completed=100)
    logger.info(f"{_('Image mirroring')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
