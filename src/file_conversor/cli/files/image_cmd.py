
# src\file_conversor\cli\multimedia\image_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Callable, List

from rich import print
from rich.panel import Panel
from rich.console import Group

# user-provided modules
from file_conversor.backend.image import *

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.progress_manager import ProgressManager
from file_conversor.utils.validators import *

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

image_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    # compress commands
    for ext in CompressBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="compress",
                description="Compress",
                command=f'{Environment.get_executable()} image compress "%1" -q 90',
                icon=str(icons_folder_path / 'compress.ico'),
            ),
        ])
    # IMG2PDF commands
    for ext in Img2PDFBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_pdf",
                description="To PDF",
                command=f'{Environment.get_executable()} image to-pdf "%1"',
                icon=str(icons_folder_path / "pdf.ico"),
            ),
        ])
    # PyMuSVGBackend commands
    for ext in PyMuSVGBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_jpg",
                description="To JPG",
                command=f'{Environment.get_executable()} image render "%1" -f "jpg"',
                icon=str(icons_folder_path / 'jpg.ico'),
            ),
            WinContextCommand(
                name="to_png",
                description="To PNG",
                command=f'{Environment.get_executable()} image render "%1" -f "png"',
                icon=str(icons_folder_path / 'png.ico'),
            ),
        ])
    # Pillow commands
    for ext in PillowBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="info",
                description="Get Info",
                command=f'cmd /k "{Environment.get_executable()} image info "%1""',
                icon=str(icons_folder_path / "info.ico"),
            ),
            WinContextCommand(
                name="to_jpg",
                description="To JPG",
                command=f'{Environment.get_executable()} image convert "%1" -f "jpg" -q 90',
                icon=str(icons_folder_path / 'jpg.ico'),
            ),
            WinContextCommand(
                name="to_png",
                description="To PNG",
                command=f'{Environment.get_executable()} image convert "%1" -f "png" -q 90',
                icon=str(icons_folder_path / 'png.ico'),
            ),
            WinContextCommand(
                name="to_webp",
                description="To WEBP",
                command=f'{Environment.get_executable()} image convert "%1" -f "webp" -q 90',
                icon=str(icons_folder_path / 'webp.ico'),
            ),
            WinContextCommand(
                name="rotate_anticlock_90",
                description="Rotate Left",
                command=f'{Environment.get_executable()} image rotate "%1" -r -90',
                icon=str(icons_folder_path / "rotate_left.ico"),
            ),
            WinContextCommand(
                name="rotate_clock_90",
                description="Rotate Right",
                command=f'{Environment.get_executable()} image rotate "%1" -r 90',
                icon=str(icons_folder_path / "rotate_right.ico"),
            ),
            WinContextCommand(
                name="mirror_x",
                description="Mirror X axis",
                command=f'{Environment.get_executable()} image mirror "%1" -a x',
                icon=str(icons_folder_path / "left_right.ico"),
            ),
            WinContextCommand(
                name="mirror_y",
                description="Mirror Y axis",
                command=f'{Environment.get_executable()} image mirror "%1" -a y',
                icon=str(icons_folder_path / "up_down.ico"),
            ),
            WinContextCommand(
                name="resize",
                description="Resize",
                command=f'cmd /k "{Environment.get_executable()} image resize "%1""',
                icon=str(icons_folder_path / "resize.ico"),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


# image compress
@image_cmd.command(
    help=f"""
        {_('Compress an image file (requires external libraries).')}

        {_('Outputs an image file with _compressed at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor image compress input_file.jpg -q 85`

        - `file_conversor image compress input_file.png -od D:/Downloads -o`
    """)
def compress(
    input_files: Annotated[List[Path], typer.Argument(
        help=f"{_('Input files')} ({', '.join(CompressBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, CompressBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    quality: Annotated[int, typer.Option("--quality", "-q",
                                         help=_("Image quality (valid only for JPG). Valid values are between 1-100."),
                                         min=1, max=100,
                                         )] = CONFIG["image-quality"],

    output_dir: Annotated[Path, typer.Option("--output-dir", "-od",
                                             help=f"{_('Output directory')}. {_('Defaults to current working directory')}.",
                                             callback=lambda x: check_dir_exists(x, mkdir=True),
                                             )] = Path(),
):
    compress_backend = CompressBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )
    with ProgressManager(len(input_files)) as progress_mgr:
        for input_file in input_files:
            output_file = output_dir / Environment.get_output_file(input_file, "_compressed")
            if not STATE["overwrite"]:
                check_path_exists(output_file, exists=False)

            logger.info(f"Processing '{output_file}' ... ")
            compress_backend.compress(
                input_file=input_file,
                output_file=output_file,
                quality=quality,
            )
            progress_mgr.complete_step()
    logger.info(f"{_('Image compression')}: [green bold]{_('SUCCESS')}[/]")


# image info
@image_cmd.command(
    help=f"""
        {_('Get EXIF information about a image file.')}

        {_('This command retrieves metadata and other information about the image file')}:
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor image info other_filename.jpg`

        - `file_conversor image info filename.webp filename2.png filename3.gif`
    """)
def info(
    input_files: Annotated[List[Path], typer.Argument(
        help=f"{_('Input files')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])
    for input_file in input_files:
        formatted = []
        in_ext = Path(input_file).suffix[1:]

        logger.info(f"{_('Parsing metadata for')} '{input_file}' ...")
        metadata = pillow_backend.info(input_file)

        # 📁 Informações gerais do arquivo
        formatted.append(f"  - {_('Name')}: {input_file}")
        formatted.append(f"  - {_('Format')}: {in_ext.upper()}")
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

        - `file_conversor image to-pdf input_file.jpg -of output_file.pdf --dpi 96`

        - `file_conversor image to-pdf input_file1.bmp input_file2.png -of output_file.pdf`

        - `file_conversor image to-pdf input_file.jpg -of output_file.pdf -ps a4_landscape`

        - `file_conversor image to-pdf input_file1.bmp input_file2.png -of output_file.pdf --page-size (21.00,29.70)`
    """)
def to_pdf(
    input_files: Annotated[List[Path], typer.Argument(help=f"{_('Input files')} ({', '.join(Img2PDFBackend.SUPPORTED_IN_FORMATS)})",
                                                      callback=lambda x: check_file_format(x, Img2PDFBackend.SUPPORTED_IN_FORMATS, exists=True),
                                                      )],

    dpi: Annotated[int, typer.Option("--dpi", "-d",
                                     help=_("Image quality in dots per inch (DPI). Valid values are between 40-3600."),
                                     min=40, max=3600,
                                     )] = CONFIG["image-dpi"],

    fit: Annotated[str, typer.Option("--fit", "-f",
                                     help=f"{_("Image fit. Valid only if ``--page-size`` is defined. Valid values are")} {", ".join(Img2PDFBackend.FIT_MODES)}. {_("Defaults to")} {CONFIG["image-fit"]}",
                                     callback=lambda x: check_valid_options(x.lower(), Img2PDFBackend.FIT_MODES),
                                     )] = CONFIG["image-fit"],

    page_size: Annotated[str | None, typer.Option("--page-size", "-ps",
                                                  help=f"{_("Page size. Format '(width, height)'. Other valid values are:")} {", ".join(Img2PDFBackend.PAGE_LAYOUT)}. {_("Defaults to None (PDF size = image size).")}",
                                                  callback=lambda x: check_valid_options(x.lower() if x else None, Img2PDFBackend.PAGE_LAYOUT),
                                                  )] = CONFIG["image-page-size"],

    set_metadata: Annotated[bool, typer.Option("--set-metadata", "-sm",
                                               help=_("Set PDF metadata. Defaults to False (do not set creator, producer, modification date, etc)."),
                                               callback=check_is_bool_or_none,
                                               is_flag=True,
                                               )] = False,

    output_file: Annotated[Path | None, typer.Option("--output-file", "-of",
                                                     help=f"{_('Output file')} ({', '.join(Img2PDFBackend.SUPPORTED_OUT_FORMATS)}). {_('Defaults to None')} ({_('use the same 1st input file as output name')}).",
                                                     callback=lambda x: check_file_format(x, Img2PDFBackend.SUPPORTED_OUT_FORMATS),
                                                     )] = None,
):
    output_file = output_file if output_file else Path() / Environment.get_output_file(input_files[0], "", "pdf")
    if not STATE["overwrite"]:
        check_path_exists(output_file, exists=False)

    img2pdf_backend = Img2PDFBackend(verbose=STATE['verbose'])
    # display current progress
    with ProgressManager() as progress_mgr:
        page_sz: tuple | None = None
        if page_size in Img2PDFBackend.PAGE_LAYOUT:
            page_sz = Img2PDFBackend.PAGE_LAYOUT[page_size]
        elif page_size:
            page_sz = tuple(page_size)

        img2pdf_backend.to_pdf(
            input_files=input_files,
            output_file=output_file,
            dpi=dpi,
            image_fit=Img2PDFBackend.FIT_MODES[fit],
            page_size=page_sz,
            include_metadata=set_metadata,
        )
        progress_mgr.complete_step()
    logger.info(f"{_('PDF generation')}: [green bold]{_('SUCCESS')}[/]")


# image render
@image_cmd.command(
    help=f"""
        {_('Render an image vector file into a different format.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor image render input_file.svg -f png`

        - `file_conversor image render input_file.svg input_file2.svg -od D:/Downloads -f jpg --dpi 300`
    """)
def render(
    input_files: Annotated[List[Path], typer.Argument(
        help=f"{_('Input files')} ({', '.join(PyMuSVGBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PyMuSVGBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    format: Annotated[str, typer.Option("--format", "-f",
                                        help=f"{_('Output format')} ({', '.join(PyMuSVGBackend.SUPPORTED_OUT_FORMATS)})",
                                        callback=lambda x: check_valid_options(x, PyMuSVGBackend.SUPPORTED_OUT_FORMATS),
                                        )],

    dpi: Annotated[int, typer.Option("--dpi", "-d",
                                     help=_("Image quality in dots per inch (DPI). Valid values are between 40-3600."),
                                     min=40, max=3600,
                                     )] = CONFIG["image-dpi"],

    output_dir: Annotated[Path, typer.Option("--output-dir", "-od",
                                             help=f"{_('Output directory')}. {_('Defaults to current working directory')}.",
                                             callback=lambda x: check_dir_exists(x, mkdir=True),
                                             )] = Path(),
):
    pymusvg_backend = PyMuSVGBackend(verbose=STATE['verbose'])
    # display current progress
    with ProgressManager(len(input_files)) as progress_mgr:
        for input_file in input_files:
            output_file = output_dir / Environment.get_output_file(input_file, suffix=f".{format}")
            if not STATE["overwrite"]:
                check_path_exists(output_file, exists=False)

            print(f"Processing '{output_file}' ... ")
            pymusvg_backend.convert(
                input_file=input_file,
                output_file=output_file,
                dpi=dpi,
            )
            progress_mgr.complete_step()
    logger.info(f"{_('Image render')}: [green bold]{_('SUCCESS')}[/]")


# image convert
@image_cmd.command(
    help=f"""
        {_('Convert a image file to a different format.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor image convert input_file.webp -f jpg --quality 85`

        - `file_conversor image convert input_file.bmp -f png -od D:/Downloads`
    """)
def convert(
    input_files: Annotated[List[Path], typer.Argument(
        help=f"{_('Input files')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    format: Annotated[str, typer.Option("--format", "-f",
                                        help=f"{_('Output format')} ({', '.join(PillowBackend.SUPPORTED_OUT_FORMATS)})",
                                        callback=lambda x: check_valid_options(x, PillowBackend.SUPPORTED_OUT_FORMATS),
                                        )],

    quality: Annotated[int, typer.Option("--quality", "-q",
                                         help=_("Image quality. Valid values are between 1-100."),
                                         min=1, max=100,
                                         )] = CONFIG["image-quality"],

    output_dir: Annotated[Path, typer.Option("--output-dir", "-od",
                                             help=f"{_('Output directory')}. {_('Defaults to current working directory')}.",
                                             callback=lambda x: check_dir_exists(x, mkdir=True),
                                             )] = Path(),
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])
    # display current progress
    with ProgressManager(len(input_files)) as progress_mgr:
        for input_file in input_files:
            output_file = output_dir / Environment.get_output_file(input_file, suffix=f".{format}")
            if not STATE["overwrite"]:
                check_path_exists(output_file, exists=False)

            print(f"Processing '{output_file}' ... ")
            pillow_backend.convert(
                input_file=input_file,
                output_file=output_file,
                quality=quality,
            )
            progress_mgr.complete_step()
    logger.info(f"{_('Image convertion')}: [green bold]{_('SUCCESS')}[/]")


# image rotate
@image_cmd.command(
    help=f"""
        {_('Rotate a image file (clockwise or anti-clockwise).')}

        {_('Outputs an image file with _rotated at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor image rotate input_file.jpg -od D:/Downloads -r 90`

        - `file_conversor image rotate input_file.jpg -r -180 -o`
    """)
def rotate(
    input_files: Annotated[List[Path], typer.Argument(
        help=f"{_('Input files')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    rotation: Annotated[int, typer.Option("--rotation", "-r",
                                          help=_("Rotation in degrees. Valid values are between -360 (anti-clockwise rotation) and 360 (clockwise rotation)."),
                                          min=-360, max=360,
                                          )],

    resampling: Annotated[str, typer.Option("--resampling", "-re",
                                            help=f'{_("Resampling algorithm. Valid values are")} {", ".join(PillowBackend.RESAMPLING_OPTIONS)}. {_("Defaults to")} {CONFIG["image-resampling"]}.',
                                            callback=lambda x: check_valid_options(x, PillowBackend.RESAMPLING_OPTIONS),
                                            )] = CONFIG["image-resampling"],

    output_dir: Annotated[Path, typer.Option("--output-dir", "-od",
                                             help=f"{_('Output directory')}. {_('Defaults to current working directory')}.",
                                             callback=lambda x: check_dir_exists(x, mkdir=True),
                                             )] = Path(),
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])
    # display current progress
    with ProgressManager(len(input_files)) as progress_mgr:
        for input_file in input_files:
            output_file = output_dir / Environment.get_output_file(input_file, stem="_rotated")
            if not STATE["overwrite"]:
                check_path_exists(output_file, exists=False)

            print(f"Processing '{output_file}' ... ")
            pillow_backend.rotate(
                input_file=input_file,
                output_file=output_file,
                rotate=rotation,
                resampling=PillowBackend.RESAMPLING_OPTIONS[resampling],
            )
            progress_mgr.complete_step()
    logger.info(f"{_('Image rotation')}: [green bold]{_('SUCCESS')}[/]")


# image mirror
@image_cmd.command(
    help=f"""
        {_('Mirror an image file (vertically or horizontally).')}

        {_('Outputs an image file with _mirrored at the end.')}
""",
    epilog=f"""
        **{_('Examples')}:**

        - `file_conversor image mirror input_file.jpg -od D:/Downloads -a x`

        - `file_conversor image mirror input_file.png -a y -o`
    """)
def mirror(
    input_files: Annotated[List[Path], typer.Argument(
        help=f"{_('Input files')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    axis: Annotated[str, typer.Option("--axis", "-a",
                                      help=_("Axis. Valid values are 'x' (mirror horizontally) or 'y' (flip vertically)."),
                                      callback=lambda x: check_valid_options(x, valid_options=['x', 'y']),
                                      )],

    output_dir: Annotated[Path, typer.Option("--output-dir", "-od",
                                             help=f"{_('Output directory')}. {_('Defaults to current working directory')}.",
                                             callback=lambda x: check_dir_exists(x, mkdir=True),
                                             )] = Path(),
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])
    # display current progress
    with ProgressManager(len(input_files)) as progress_mgr:
        for input_file in input_files:
            output_file = output_dir / Environment.get_output_file(input_file, stem="_mirrored")
            if not STATE["overwrite"]:
                check_path_exists(output_file, exists=False)

            print(f"Processing '{output_file}' ... ")
            pillow_backend.mirror(
                input_file=input_file,
                output_file=output_file,
                x_y=True if axis == "x" else False,
            )
            progress_mgr.complete_step()
    logger.info(f"{_('Image mirroring')}: [green bold]{_('SUCCESS')}[/]")


# image resize
@image_cmd.command(
    help=f"""
        {_('Resize an image file.')}

        {_('Outputs an image file with _resized at the end.')}
""",
    epilog=f"""
        **{_('Examples')}:**



        *{_('Double the image size')}*:

        - `file_conversor image resize input_file.jpg -s 2.0`



        *{_('Set the image width to 1024px')}*:

        - `file_conversor image resize input_file.jpg -od D:/Downloads -w 1024`
    """)
def resize(
    input_files: Annotated[List[Path], typer.Argument(
        help=f"{_('Input files')} ({', '.join(PillowBackend.SUPPORTED_IN_FORMATS)})",
        callback=lambda x: check_file_format(x, PillowBackend.SUPPORTED_IN_FORMATS, exists=True),
    )],

    scale: Annotated[float | None, typer.Option("--scale", "-s",
                                                help=f"{_("Scale image proportion. Valid values start at 0.1. Defaults to")} None (use width to scale image).",
                                                callback=lambda x: check_positive_integer(x),
                                                )] = None,

    width: Annotated[int | None, typer.Option("--width", "-w",
                                              help=f"{_("Width in pixels (height is calculated based on width to keep image proportions). Defaults to")} None ({_('use scale to resize image')}).",
                                              callback=lambda x: check_positive_integer(x),
                                              )] = None,

    resampling: Annotated[str, typer.Option("--resampling", "-r",
                                            help=f'{_("Resampling algorithm. Valid values are")} {", ".join(PillowBackend.RESAMPLING_OPTIONS)}. {_("Defaults to")} {CONFIG["image-resampling"]}.',
                                            callback=lambda x: check_valid_options(x, PillowBackend.RESAMPLING_OPTIONS),
                                            )] = CONFIG["image-resampling"],

    output_dir: Annotated[Path, typer.Option("--output-dir", "-od",
                                             help=f"{_('Output directory')}. {_('Defaults to current working directory')}.",
                                             callback=lambda x: check_dir_exists(x, mkdir=True),
                                             )] = Path(),
):
    pillow_backend = PillowBackend(verbose=STATE['verbose'])
    if not scale and not width:
        if STATE["quiet"]:
            raise RuntimeError(f"{_('Scale and width not provided')}")
        userinput = str(typer.prompt(f"{_('Output image scale (e.g., 1.5)')}"))
        scale = float(userinput)

    # display current progress
    with ProgressManager(len(input_files)) as progress_mgr:
        for input_file in input_files:
            output_file = output_dir / Environment.get_output_file(input_file, stem="_resized")
            if not STATE["overwrite"]:
                check_path_exists(output_file, exists=False)

            print(f"Processing '{output_file}' ... ")
            pillow_backend.resize(
                input_file=input_file,
                output_file=output_file,
                scale=scale,
                width=width,
                resampling=PillowBackend.RESAMPLING_OPTIONS[resampling],
            )
            progress_mgr.complete_step()
    logger.info(f"{_('Image resize')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
