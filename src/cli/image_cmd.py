
# src\cli\image_cmd.py

import typer

from typing import Annotated, List

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.console import Group

# user-provided modules
from backend import PillowBackend, Img2PDFBackend

from config import Configuration, State, Log
from config.locale import get_translation

from utils import File
from utils.rich import get_progress_bar
from utils.validators import check_file_format, check_is_bool_or_none, check_valid_options

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

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

        - `file_conversor image to-pdf input_file.jpg output_file.pdf --dpi 96`

        - `file_conversor image to-pdf input_file1.bmp input_file2.png output_file.pdf`

        - `file_conversor image to-pdf input_file.jpg output_file.pdf -ps a4_landscape`

        - `file_conversor image to-pdf input_file1.bmp input_file2.png output_file.pdf --page-size (21.00,29.70)`
    """)
def to_pdf(
    input_file: Annotated[List[str], typer.Argument(help=f"{_('Input files')} ({', '.join(Img2PDFBackend.SUPPORTED_IN_FORMATS)})",
                                                    callback=lambda x: check_file_format(x, Img2PDFBackend.SUPPORTED_IN_FORMATS, exists=True),
                                                    )],

    output_file: Annotated[str, typer.Argument(help=f"{_('Output file')} ({', '.join(Img2PDFBackend.SUPPORTED_OUT_FORMATS)})",
                                               callback=lambda x: check_file_format(x, Img2PDFBackend.SUPPORTED_OUT_FORMATS),
                                               )],

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
            input_files=input_file,
            output_file=output_file,
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

        - `file_conversor image convert input_file.webp output_file.jpg --quality 85`

        - `file_conversor image convert input_file.bmp output_file.png`
    """)
def convert(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    output_file: Annotated[str, typer.Argument(
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

        - `file_conversor pdf rotate input_file.jpg output_file.jpg 90` 
        
        - `file_conversor pdf rotate input_file.jpg output_file.jpg -180` 
    """)
def rotate(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    output_file: Annotated[str, typer.Argument(
        help=f"{_('Output file')} ({', '.join(PillowBackend.SUPPORTED_OUT_FORMATS)})",
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
        task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None)
        pillow_backend.rotate(
            input_file=input_file,
            output_file=output_file,
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

        - `file_conversor pdf mirror input_file.jpg output_file.jpg -a x` 
        
        - `file_conversor pdf mirror input_file.jpg output_file.jpg -a y` 
    """)
def mirror(
    input_file: Annotated[str, typer.Argument(
        help=f"{_('Input file')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    output_file: Annotated[str, typer.Argument(
        help=f"{_('Output file')} ({', '.join(PillowBackend.SUPPORTED_OUT_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_OUT_FORMATS),
    )],

    axis: Annotated[int, typer.Option("--axis", "-a",
                                      help=_("Axis. Valid values are 'x' (mirror horizontally) or 'y' (flip vertically)."),
                                      callback=lambda x: check_valid_options(x, valid_options=['x', 'y']),
                                      )],
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])
    # display current progress
    with get_progress_bar() as progress:
        task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None)
        pillow_backend.mirror(
            input_file=input_file,
            output_file=output_file,
            x_y=True if axis == "x" else False,
        )
        progress.update(task, total=100, completed=100)
    logger.info(f"{_('Image mirroring')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
