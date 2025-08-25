
# src\file_conversor\cli\multimedia\pdf_cmd.py

import tempfile
import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend.pdf import PyPDFBackend, PikePDFBackend, PyMuPDFBackend, GhostscriptBackend

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.formatters import parse_pdf_pages, parse_pdf_rotation
from file_conversor.utils.validators import *
from file_conversor.utils.typer import *

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

# typer PANELS
SECURITY_PANEL = _(f"Security commands")

pdf_cmd = typer.Typer()


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    ctx_menu.add_extension(".pdf", [
        WinContextCommand(
            name="to_png",
            description="To PNG",
            command=f'{Environment.get_executable()} pdf convert "%1" -f "png"',
            icon=str(icons_folder_path / 'png.ico'),
        ),
        WinContextCommand(
            name="to_jpg",
            description="To JPG",
            command=f'{Environment.get_executable()} pdf convert "%1" -f "jpg"',
            icon=str(icons_folder_path / 'jpg.ico'),
        ),
        WinContextCommand(
            name="compress",
            description="Compress",
            command=f'{Environment.get_executable()} pdf compress "%1"',
            icon=str(icons_folder_path / 'compress.ico'),
        ),
        WinContextCommand(
            name="repair",
            description="Repair",
            command=f'{Environment.get_executable()} pdf repair "%1"',
            icon=str(icons_folder_path / 'repair.ico'),
        ),
        WinContextCommand(
            name="split",
            description="Split",
            command=f'{Environment.get_executable()} pdf split "%1"',
            icon=str(icons_folder_path / 'split.ico'),
        ),
        WinContextCommand(
            name="extract",
            description="Extract",
            command=f'cmd /k "{Environment.get_executable()} pdf extract "%1""',
            icon=str(icons_folder_path / 'extract.ico'),
        ),
        WinContextCommand(
            name="extract_img",
            description="Extract IMG",
            command=f'{Environment.get_executable()} pdf extract-img "%1"',
            icon=str(icons_folder_path / 'separate.ico'),
        ),
        WinContextCommand(
            name="rotate_anticlock_90",
            description="Rotate Left",
            command=f'{Environment.get_executable()} pdf rotate "%1" -r "1-:-90"',
            icon=str(icons_folder_path / "rotate_left.ico"),
        ),
        WinContextCommand(
            name="rotate_clock_90",
            description="Rotate Right",
            command=f'{Environment.get_executable()} pdf rotate "%1" -r "1-:90"',
            icon=str(icons_folder_path / "rotate_right.ico"),
        ),
        WinContextCommand(
            name="encrypt",
            description="Encrypt",
            command=f'cmd /k "{Environment.get_executable()} pdf encrypt "%1""',
            icon=str(icons_folder_path / "padlock_locked.ico"),
        ),
        WinContextCommand(
            name="decrypt",
            description="Decrypt",
            command=f'cmd /k "{Environment.get_executable()} pdf decrypt "%1""',
            icon=str(icons_folder_path / "padlock_unlocked.ico"),
        ),
    ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


# pdf repair
@pdf_cmd.command(
    help=f"""
        {_('Repair (lightly) corrupted PDF files.')}        
        
        {_('Outputs a file with _repaired at the end.')}
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor pdf repair input_file.pdf -od D:/Downloads` 
""")
def repair(
    input_files: InputFilesArgument(PikePDFBackend),  # pyright: ignore[reportInvalidTypeForm]
    password: PasswordOption() = None,  # pyright: ignore[reportInvalidTypeForm]
    output_dir: OutputDirOption() = Path(),  # pyright: ignore[reportInvalidTypeForm]
):
    pikepdf_backend = PikePDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        print(f"Processing '{output_file}' ... ")
        pikepdf_backend.compress(
            # files
            input_file=input_file,
            output_file=output_file,

            # options
            decrypt_password=password,
            progress_callback=progress_mgr.update_progress
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite"])
    cmd_mgr.run(callback, out_stem="_repaired")

    logger.info(f"{_('Repair PDF')}: [bold green]{_('SUCCESS')}[/].")


# pdf compress
@pdf_cmd.command(
    help=f"""
        {_('Compress a PDF file (requires Ghostscript external library).')}
        
        {_('Outputs a file with _compressed at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor pdf compress input_file.pdf -od D:/Downloads`

        - `file_conversor pdf compress input_file.pdf -c high`

        - `file_conversor pdf compress input_file.pdf -o`
    """)
def compress(
    input_files: InputFilesArgument(GhostscriptBackend),  # pyright: ignore[reportInvalidTypeForm]
    compression: Annotated[str, typer.Option("--compression", "-c",
                                             help=f"{_('Compression level (high compression = low quality). Valid values are')} {', '.join(GhostscriptBackend.Compression.get_dict())}. {_('Defaults to')} {CONFIG["pdf-compression"]}.",
                                             callback=lambda x: check_valid_options(x, GhostscriptBackend.Compression.get_dict()),
                                             )] = CONFIG["pdf-compression"],
    output_dir: OutputDirOption() = Path(),  # pyright: ignore[reportInvalidTypeForm]
):
    pikepdf_backend = PikePDFBackend(verbose=STATE["verbose"])
    gs_backend = GhostscriptBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE['verbose'],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        with tempfile.TemporaryDirectory() as temp_dir:
            gs_out = Path(temp_dir) / CommandManager.get_output_file(input_file, stem="_gs")
            gs_backend.compress(
                input_file=input_file,
                output_file=gs_out,
                compression_level=GhostscriptBackend.Compression.from_str(compression),
                progress_callback=progress_mgr.update_progress
            )
            progress_mgr.complete_step()

            pikepdf_backend.compress(
                # files
                input_file=gs_out,
                output_file=output_file,
                progress_callback=progress_mgr.update_progress
            )
            progress_mgr.complete_step()
            print(f"Processing '{output_file}' ... OK")
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, steps=2, overwrite=STATE["overwrite"])
    cmd_mgr.run(callback, out_stem="_compressed")

    logger.info(f"{_('File compression')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


# pdf convert
@pdf_cmd.command(
    help=f"""
        {_('Convert a PDF file to a different format.')}        
        
        {_('Outputs a file with the PDF page number at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor pdf convert input_file.pdf -f jpg --dpi 200`

        - `file_conversor pdf convert input_file.pdf -f png -o`
    """)
def convert(
    input_files: InputFilesArgument(PyMuPDFBackend),  # pyright: ignore[reportInvalidTypeForm]
    format: FormatOption(PyMuPDFBackend),  # pyright: ignore[reportInvalidTypeForm]
    dpi: DPIOption() = CONFIG["image-dpi"],  # pyright: ignore[reportInvalidTypeForm]
    output_dir: OutputDirOption() = Path(),  # pyright: ignore[reportInvalidTypeForm]
):
    pymupdf_backend = PyMuPDFBackend(verbose=STATE['verbose'])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        print(f"Processing '{output_file}' ...")
        pymupdf_backend.convert(
            input_file=input_file,
            output_file=output_file,
            dpi=dpi,
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite"])
    cmd_mgr.run(callback, out_suffix=f".{format}")

    logger.info(f"{_('File convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


# pdf merge
@pdf_cmd.command(
    help=f"""
        {_('Merge (join) input PDFs into a single PDF file.')}
        
        {_('Outputs a file with _merged at the end.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Merge files "input_file1.pdf" and "input_file2.pdf" into "output_file.pdf"')}*:

- `file_conversor pdf merge "input_file1.pdf" "input_file2.pdf" -of output_file.pdf` 



*{_('Merge protected PDFs "input_file1.pdf" and "input_file2.pdf" with password "unlock_password"')}*:

- `file_conversor pdf merge "input_file1.pdf" "input_file2.pdf" -p "unlock_password" -of output_file.pdf` 
    """)
def merge(
    input_files: InputFilesArgument(PyPDFBackend),  # pyright: ignore[reportInvalidTypeForm]
    password: PasswordOption() = None,  # pyright: ignore[reportInvalidTypeForm]
    output_file: OutputFileOption(PyPDFBackend) = None,  # pyright: ignore[reportInvalidTypeForm]
):
    output_file = output_file if output_file else Path() / CommandManager.get_output_file(input_files[0], stem="_merged")
    if not STATE["overwrite"]:
        check_path_exists(output_file, exists=False)

    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with ProgressManager() as progress_mgr:
        print(f"Processing '{output_file}' ...")
        pypdf_backend.merge(
            # files
            input_files=input_files,
            output_file=output_file,
            password=password,
            progress_callback=progress_mgr.update_progress
        )
        progress_mgr.complete_step()

    logger.info(f"{_('Merge pages')}: [bold green]{_('SUCCESS')}[/].")


# pdf split
@pdf_cmd.command(
    help=f"""
        {_('Split PDF pages into several 1-page PDFs.')}

        {_('For every PDF page, a new single page PDF will be created using the format `input_file_X.pdf`, where X is the page number.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Split pages of input_file.pdf into output_file_X.pdf files')}*:

- `file_conversor pdf split input_file.pdf -od D:/Downloads` 



*{_('For every PDF page, generate a "input_file_X.pdf" file')}*:

- `file_conversor pdf split input_file.pdf` 
""")
def split(
    input_files: InputFilesArgument(PyPDFBackend),  # pyright: ignore[reportInvalidTypeForm]
    password: PasswordOption() = None,  # pyright: ignore[reportInvalidTypeForm]
    output_dir: OutputDirOption() = Path(),  # pyright: ignore[reportInvalidTypeForm]
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        print(f"Processing '{output_file}' ... ")
        pypdf_backend.split(
            input_file=input_file,
            output_file=output_file,
            password=password,
            progress_callback=progress_mgr.update_progress,
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite"])
    cmd_mgr.run(callback)
    logger.info(f"{_('Split pages')}: [bold green]{_('SUCCESS')}[/].")


# pdf extract
@pdf_cmd.command(
    help=f"""
        {_('Extract specific pages from a PDF.')}
        
        {_('Outputs a file with _extracted at the end.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Extract pages 1 to 2, 4 and 6')}*:

- `file_conversor pdf extract input_file.pdf -pg 1-2 -pg 4-4 -pg 6-6 -od D:/Downloads` 
    """)
def extract(
    input_files: InputFilesArgument(PyPDFBackend),  # pyright: ignore[reportInvalidTypeForm]
    pages: Annotated[List[str] | None, typer.Option("--pages", "-pg",
                                                    help=_('Pages to extract (comma-separated list). Format "start-end".'),
                                                    )] = None,
    password: PasswordOption() = None,  # pyright: ignore[reportInvalidTypeForm]
    output_dir: OutputDirOption() = Path(),  # pyright: ignore[reportInvalidTypeForm]
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        pypdf_backend.extract(
            input_file=input_file,
            output_file=output_file,
            password=password,
            pages=parse_pdf_pages(pages),
            progress_callback=progress_mgr.update_progress
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite"])
    cmd_mgr.run(callback, out_stem="_extracted")
    logger.info(f"{_('Extract pages')}: [bold green]{_('SUCCESS')}[/].")


# pdf extract-img
@pdf_cmd.command(
    help=f"""
        {_('Extract images from a PDF.')}
        
        {_('For every PDF page, a new image file will be created using the format `input_file_X`, where X is the page number.')}
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor pdf extract-img input_file.pdf -od D:/Downloads` 
    """)
def extract_img(
    input_files: InputFilesArgument(PyMuPDFBackend),  # pyright: ignore[reportInvalidTypeForm]
    output_dir: OutputDirOption() = Path(),  # pyright: ignore[reportInvalidTypeForm]
):
    pymupdf_backend = PyMuPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        pymupdf_backend.extract_images(
            # files
            input_file=input_file,
            output_dir=output_dir,
            overwrite_files=STATE["overwrite"],
            progress_callback=progress_mgr.update_progress
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite"])
    cmd_mgr.run(callback)
    logger.info(f"{_('Extract images')}: [bold green]{_('SUCCESS')}[/].")


# pdf rotate
@pdf_cmd.command(
    help=f"""
        {_('Rotate PDF pages (clockwise or anti-clockwise).')}
        
        {_('Outputs a file with _rotated at the end.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Rotate page 1 by 180 degress')}*:

- `file_conversor pdf rotate input_file.pdf -o output_file.pdf -r "1:180"` 



*{_('Rotate page 5-7 by 90 degress, 9 by -90 degrees, 10-15 by 180 degrees')}*:

- `file_conversor pdf rotate input_file.pdf -r "5-7:90" -r "9:-90" -r "10-15:180"`
    """)
def rotate(
    input_files: InputFilesArgument(PyPDFBackend),  # pyright: ignore[reportInvalidTypeForm]
    rotation: Annotated[List[str], typer.Option("--rotation", "-r",
                                                help=_("List of pages to rotate. Format ``\"page:rotation\"`` or ``\"start-end:rotation\"`` or ``\"start-:rotation\"`` ..."),
                                                )],
    password: PasswordOption() = None,  # pyright: ignore[reportInvalidTypeForm]
    output_dir: OutputDirOption() = Path(),  # pyright: ignore[reportInvalidTypeForm]
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        pypdf_backend.rotate(
            input_file=input_file,
            output_file=output_file,
            decrypt_password=password,
            rotations=parse_pdf_rotation(rotation, pypdf_backend.len(input_file)),
            progress_callback=progress_mgr.update_progress
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite"])
    cmd_mgr.run(callback, out_stem="_rotated")
    logger.info(f"{_('Rotate pages')}: [bold green]{_('SUCCESS')}[/].")


# pdf encrypt
@pdf_cmd.command(
    rich_help_panel=SECURITY_PANEL,
    help=f"""
        {_('Protect PDF file with a password (create encrypted PDF file).')}
        
        {_('Outputs a file with _encrypted at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor pdf encrypt input_file.pdf -od D:/Downloads --owner-password 1234`

        - `file_conversor pdf encrypt input_file.pdf -op 1234 --up 0000 -an -co`
    """)
def encrypt(
    input_files: InputFilesArgument(PyPDFBackend),  # pyright: ignore[reportInvalidTypeForm]
    owner_password: Annotated[str, typer.Option("--owner-password", "-op",
                                                help=_("Owner password for encryption. Owner has ALL PERMISSIONS in the output PDF file."),
                                                prompt=f"{_('Owner password for encryption (password will not be displayed, for your safety)')}",
                                                hide_input=True,
                                                )],

    user_password: Annotated[str | None, typer.Option("--user-password", "-up",
                                                      help=_("User password for encryption. User has ONLY THE PERMISSIONS specified in the arguments. Defaults to None (user and owner password are the same)."),
                                                      )] = None,
    decrypt_password: Annotated[str | None, typer.Option("--decrypt-password", "-dp",
                                                         help=_("Decrypt password used to open protected file. Defaults to None (do not decrypt)."),
                                                         )] = None,

    allow_annotate: Annotated[bool, typer.Option("--annotate", "-an",
                                                 help=_("User can add/modify annotations (comments, highlight text, etc) and interactive forms. Default to False (not set)."),
                                                 is_flag=True,
                                                 )] = False,
    allow_fill_forms: Annotated[bool, typer.Option("--fill-forms", "-ff",
                                                   help=_("User can fill form fields (subset permission of --annotate). Default to False (not set)."),
                                                   is_flag=True,
                                                   )] = False,
    allow_modify: Annotated[bool, typer.Option("--modify", "-mo",
                                               help=_("User can modify the document (e.g., add / edit text, add / edit images, etc). Default to False (not set)."),
                                               is_flag=True,
                                               )] = False,
    allow_modify_pages: Annotated[bool, typer.Option("--modify-pages", "-mp",
                                                     help=_("User can insert, delete, or rotate pages (subset of --modify). Default to False (not set)."),
                                                     is_flag=True,
                                                     )] = False,
    allow_copy: Annotated[bool, typer.Option("--copy", "-co",
                                             help=_("User can copy text/images. Default to False (not set)."),
                                             is_flag=True,
                                             )] = False,
    allow_accessibility: Annotated[bool, typer.Option("--accessibility", "-ac",
                                                      help=_("User can use screen readers for accessibility. Default to True (allow)."),
                                                      is_flag=True,
                                                      )] = True,
    allow_print_lq: Annotated[bool, typer.Option("--print-lq", "-pl",
                                                 help=_("User can print (low quality). Defaults to True (allow)."),
                                                 is_flag=True,
                                                 )] = True,
    allow_print_hq: Annotated[bool, typer.Option("--print-hq", "-ph",
                                                 help=_("User can print (high quality). Requires --allow-print. Defaults to True (allow)."),
                                                 is_flag=True,
                                                 )] = True,
    allow_all: Annotated[bool, typer.Option("--all", "-all",
                                            help=_("User has ALL PERMISSIONS. If set, it overrides all other permissions. Defaults to False (not set)."),
                                            is_flag=True,
                                            )] = False,
    encrypt_algo: Annotated[str, typer.Option("--encryption", "-enc",
                                              help=_("Encryption algorithm used. Valid options are RC4-40, RC4-128, AES-128, AES-256-R5, or AES-256. Defaults to AES-256 (for enhanced security and compatibility)."),
                                              callback=lambda x: check_valid_options(x, valid_options=[None, "RC4-40", "RC4-128", "AES-128", "AES-256-R5", "AES-256"])
                                              )] = "AES-256",

    output_dir: OutputDirOption() = Path(),  # pyright: ignore[reportInvalidTypeForm]
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        pypdf_backend.encrypt(
            # files
            input_file=input_file,
            output_file=output_file,

            # passwords
            owner_password=owner_password,
            user_password=user_password,
            decrypt_password=decrypt_password,

            # permissions
            permission_annotate=allow_annotate,
            permission_fill_forms=allow_fill_forms,
            permission_modify=allow_modify,
            permission_modify_pages=allow_modify_pages,
            permission_copy=allow_copy,
            permission_accessibility=allow_accessibility,
            permission_print_low_quality=allow_print_lq,
            permission_print_high_quality=allow_print_hq,
            permission_all=allow_all,

            encryption_algorithm=encrypt_algo,
            progress_callback=progress_mgr.update_progress
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite"])
    cmd_mgr.run(callback, out_stem="_encrypted")
    logger.info(f"{_('Encryption')}: [bold green]{_('SUCCESS')}[/].")


# pdf decrypt
@pdf_cmd.command(
    rich_help_panel=SECURITY_PANEL,
    help=f"""
        {_('Remove password protection from a PDF file  (create decrypted PDF file).')}        
        
        {_('Outputs a file with _decrypted at the end.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor pdf decrypt input_file.pdf input_file2.pdf --password 1234`

        - `file_conversor pdf decrypt input_file.pdf -p 1234`
    """)
def decrypt(
    input_files: InputFilesArgument(PyPDFBackend),  # pyright: ignore[reportInvalidTypeForm]
    password: Annotated[str, typer.Option("--password", "-p",
                                          help=_("Password used for decryption."),
                                          prompt=f"{_('Password for decryption (password will not be displayed, for your safety)')}",
                                          hide_input=True,
                                          )],
    output_dir: OutputDirOption() = Path(),  # pyright: ignore[reportInvalidTypeForm]
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        pypdf_backend.decrypt(
            input_file=input_file,
            output_file=output_file,
            password=password,
            progress_callback=progress_mgr.update_progress
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite"])
    cmd_mgr.run(callback, out_stem="_decrypted")
    logger.info(f"{_('Decryption')}: [bold green]{_('SUCCESS')}[/].")
