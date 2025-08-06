
# src\cli\pdf_cmd.py

import re
import time
import typer

from pathlib import Path
from typing import Annotated, List

from rich import print

# user-provided modules
from file_conversor.backend import PyPDFBackend, QPDFBackend

from file_conversor.config import Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.rich import get_progress_bar
from file_conversor.utils.validators import check_file_format, check_valid_options

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
    icons_folder_path = State.get_icons_folder()
    ctx_menu.add_extension(".pdf", [
        WinContextCommand(
            name="repair",
            description="Repair",
            command=f'{State.get_executable()} pdf repair "%1"',
            icon=str(icons_folder_path / 'repair.ico'),
        ),
        WinContextCommand(
            name="split",
            description="Split",
            command=f'{State.get_executable()} pdf split "%1"',
            icon=str(icons_folder_path / 'split.ico'),
        ),
        WinContextCommand(
            name="extract",
            description="Extract",
            command=f'cmd /k "{State.get_executable()} pdf extract "%1""',
            icon=str(icons_folder_path / 'extract.ico'),
        ),
        WinContextCommand(
            name="rotate_clock_90",
            description="Rotate Left",
            command=f'{State.get_executable()} pdf rotate "%1" -r "1-:90"',
            icon=str(icons_folder_path / "rotate_left.ico"),
        ),
        WinContextCommand(
            name="rotate_anticlock_90",
            description="Rotate Right",
            command=f'{State.get_executable()} pdf rotate "%1" -r "1-:-90"',
            icon=str(icons_folder_path / "rotate_right.ico"),
        ),
        WinContextCommand(
            name="encrypt",
            description="Encrypt",
            command=f'cmd /k "{State.get_executable()} pdf encrypt "%1""',
            icon=str(icons_folder_path / "padlock_locked.ico"),
        ),
        WinContextCommand(
            name="decrypt",
            description="Decrypt",
            command=f'cmd /k "{State.get_executable()} pdf decrypt "%1""',
            icon=str(icons_folder_path / "padlock_unlocked.ico"),
        ),
    ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance(CONFIG['install-context-menu-all-users'])
ctx_menu.register_callback(register_ctx_menu)


# pdf repair
@pdf_cmd.command(
    help=f"""
        {_('Repair (lightly) corrupted PDF files (requires QPDF external library).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor pdf repair input_file.pdf -o output_file.pdf` 
""")
def repair(
    input_file: Annotated[str, typer.Argument(help=f"{_('Input file')} ({', '.join(QPDFBackend.SUPPORTED_IN_FORMATS)})",
                                              callback=lambda x: check_file_format(x, QPDFBackend.SUPPORTED_IN_FORMATS, exists=True),
                                              )],
    output_file: Annotated[str | None, typer.Option("--output", "-o",
                                                    help=f"{_('Output file')} ({', '.join(QPDFBackend.SUPPORTED_IN_FORMATS)}). {_('Defaults to None')} ({_('use the same input file as output name')}, {_('with _repaired.pdf at the end)')}.",
                                                    callback=lambda x: check_file_format(x, QPDFBackend.SUPPORTED_OUT_FORMATS),
                                                    )] = None,
    decrypt_password: Annotated[str | None, typer.Option("--password", "-p",
                                                         help=_("Password used to open protected file. Defaults to None (do not decrypt)."),
                                                         )] = None,
    compress: Annotated[bool, typer.Option("--compress", "-c",
                                           help=_("Compress output PDF file (losslessly). Defaults to True (compress)."),
                                           is_flag=True,
                                           )] = True,
):
    qpdf_backend = QPDFBackend(verbose=STATE["verbose"], install_deps=CONFIG['install-deps'])
    with get_progress_bar() as progress:
        task1 = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None,)

        process = qpdf_backend.repair(
            # files
            input_file=input_file,
            output_file=output_file if output_file else f"{input_file.replace(".pdf", "")}_repaired.pdf",

            # options
            decrypt_password=decrypt_password,
            compress=compress,
        )
        while process.poll() is None:
            time.sleep(0.25)
        progress.update(task1, total=100, completed=100)

    process.wait()
    if process.returncode != 0:
        raise RuntimeError(qpdf_backend.dump_streams(process))

    logger.info(f"{_('Repair PDF')}: [bold green]{_('SUCCESS')}[/].")


# pdf merge
@pdf_cmd.command(
    help=f"""
        {_('Merge (join) input PDFs into a single PDF file.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Merge files "input_file1.pdf" and "input_file2.pdf" into "output_file.pdf"')}*:

- `file_conversor pdf merge "input_file1.pdf" "input_file2.pdf" -o output_file.pdf` 



*{_('Merge protected PDF "input_file1.pdf" with password "unlock_password" with unprotected file "input_file2.pdf"')}*:

- `file_conversor pdf merge "input_file1.pdf:unlock_password" "input_file2.pdf" -o output_file.pdf` 
    """)
def merge(
    input_files: Annotated[List[str], typer.Argument(help=f"{_('Input file')} ({', '.join(PyPDFBackend.SUPPORTED_IN_FORMATS)}). {_('If file is protected, provide its password using the format `"filepath:password"`')}.",
                                                     )],
    output_file: Annotated[str | None, typer.Option("--output", "-o",
                                                    help=f"{_("Output file")} ({', '.join(PyPDFBackend.SUPPORTED_OUT_FORMATS)}). {_('Defaults to None')} ({_('use the same input file of 1st file as output name')}, {_('with _merged.pdf at the end)')}",
                                                    callback=lambda x: check_file_format(x, PyPDFBackend.SUPPORTED_OUT_FORMATS),
                                                    )] = None,
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        merge_task = progress.add_task(f"{_('Processing file')} '{output_file}':", total=None,)

        # get dict in format {filepath: password}
        filepath_dict = {}
        FILEPATH_RE = re.compile(r'^(.+?)(::(.+))?$')
        for arg in input_files:
            match = FILEPATH_RE.search(arg)
            if not match:
                raise RuntimeError(f"{_('Invalid filepath format')} '{arg}'. {_("Valid format is 'filepath:password' or 'filepath'")}.")

            # check user input
            filepath = match.group(1)
            password = match.group(3) if match.group(3) else None

            # create filepath_dict
            filepath_dict[filepath] = password

        pypdf_backend.merge(
            # files
            input_files=filepath_dict,
            output_file=output_file if output_file else f"{input_files[0].replace(".pdf", "")}_merged.pdf",
        )
        progress.update(merge_task, total=100, completed=100)

    logger.info(f"{_('Merge pages')}: [bold green]{_('SUCCESS')}[/].")


# pdf split
@pdf_cmd.command(
    help=f"""
        {_('Split PDF pages into several 1-page PDFs.')}

        {_('For every PDF page, a new single page PDF will be created using the format `output_file_X.pdf`, where X is the page number.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Split pages of input_file.pdf into output_file_X.pdf files')}*:

- `file_conversor pdf split input_file.pdf -o output_file.pdf` 



*{_('For every PDF page, generate a "input_file_X.pdf" file')}*:

- `file_conversor pdf split input_file.pdf` 
""")
def split(
    input_file: Annotated[str, typer.Argument(help=f"{_('Input file')} ({', '.join(PyPDFBackend.SUPPORTED_IN_FORMATS)})",
                                              callback=lambda x: check_file_format(x, PyPDFBackend.SUPPORTED_IN_FORMATS, exists=True),
                                              )],
    output_file: Annotated[str | None, typer.Option("--output", "-o",
                                                    help=f"{_('Output file path')} ({', '.join(PyPDFBackend.SUPPORTED_OUT_FORMATS)}). {_('Defaults to None')} ({_('use the same input file as output name')})",
                                                    callback=lambda x: check_file_format(x, PyPDFBackend.SUPPORTED_OUT_FORMATS),
                                                    )] = None,
    decrypt_password: Annotated[str | None, typer.Option("--password", "-p",
                                                         help=_("Password used to open protected file. Defaults to None (do not decrypt)."),
                                                         )] = None,
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        split_task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None,)

        pypdf_backend.split(
            # files
            input_file=input_file,
            output_file=output_file if output_file else input_file,

            # passwords
            decrypt_password=decrypt_password,
        )
        progress.update(split_task, total=100, completed=100)

    logger.info(f"{_('Split pages')}: [bold green]{_('SUCCESS')}[/].")


# pdf extract
@pdf_cmd.command(
    help=f"""
        {_('Extract specific pages from a PDF.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Extract pages 1 to 2, 4 and 6')}*:

- `file_conversor pdf extract input_file.pdf -o output_file.pdf -pg 1-2 -pg 4 -pg 6` 
    """)
def extract(
    input_file: Annotated[str, typer.Argument(help=f"{_('Input file')} ({', '.join(PyPDFBackend.SUPPORTED_IN_FORMATS)})",
                                              callback=lambda x: check_file_format(x, PyPDFBackend.SUPPORTED_IN_FORMATS, exists=True),
                                              )],
    output_file: Annotated[str | None, typer.Option("--output", "-o",
                                                    help=f"{_('Output file')} ({', '.join(PyPDFBackend.SUPPORTED_OUT_FORMATS)}) {_('Defaults to None')} ({_('use the same input file as output name')}, {_('with _extracted.pdf at the end)')}",
                                                    callback=lambda x: check_file_format(x, PyPDFBackend.SUPPORTED_OUT_FORMATS),
                                                    )] = None,
    pages: Annotated[List[str] | None, typer.Option("--pages", "-pg",
                                                    help=_('Pages to extract (comma-separated list). Format "page_num" or "start-end".'),
                                                    )] = None,
    decrypt_password: Annotated[str | None, typer.Option("--password", "-p",
                                                         help=_("Password used to open protected file. Defaults to None (do not decrypt)."),
                                                         )] = None,
):
    if not pages:
        pages_str = typer.prompt(f"{_('Pages to extract [comma-separated list] (e.g., 1-3, 7)')}")
        pages = [p.strip() for p in str(pages_str).split(",")]

    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        extract_task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None,)

        # parse user input
        pages_list = []
        PAGES_RE = re.compile(r'(\d+)(-(\d*)){0,1}')
        for arg in pages:
            match = PAGES_RE.search(arg)
            if not match:
                raise RuntimeError(f"{_('Invalid page instruction')} '{arg}'. {_("Valid format is 'begin-', 'begin-end', 'page_num'")}.")

            # check user input
            begin = int(match.group(1)) - 1
            end = begin
            if match.group(3):
                end = int(match.group(3)) - 1
            elif match.group(2):
                end = pypdf_backend.len(input_file)

            if end < begin:
                raise RuntimeError(f"{_('Invalid begin-end page interval')}. {_('End Page < Begin Page')} '{arg}'.")

            # create pages list
            for page_num in range(begin, end + 1):
                pages_list.append(page_num)

        pypdf_backend.extract(
            # files
            input_file=input_file,
            output_file=output_file if output_file else f"{input_file.replace(".pdf", "")}_extracted.pdf",

            # passwords
            decrypt_password=decrypt_password,

            # other args
            pages=pages_list
        )
        progress.update(extract_task, total=100, completed=100)

    logger.info(f"{_('Extract pages')}: [bold green]{_('SUCCESS')}[/].")


# pdf rotate
@pdf_cmd.command(
    help=f"""
        {_('Rotate PDF pages (clockwise or anti-clockwise).')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Rotate page 1 by 180 degress')}*:

- `file_conversor pdf rotate input_file.pdf -o output_file.pdf -r "1:180"` 



*{_('Rotate page 5-7 by 90 degress, 9 by -90 degrees, 10-15 by 180 degrees')}*:

- `file_conversor pdf rotate input_file.pdf -o output_file.pdf -r "5-7:90" -r "9:-90" -r "10-15:180"`
    """)
def rotate(
    input_file: Annotated[str, typer.Argument(help=f"{_('Input file')} ({', '.join(PyPDFBackend.SUPPORTED_IN_FORMATS)})",
                                              callback=lambda x: check_file_format(x, PyPDFBackend.SUPPORTED_IN_FORMATS, exists=True),
                                              )],
    rotation: Annotated[List[str], typer.Option("--rotation", "-r",
                                                help=_("List of pages to rotate. Format ``\"page:rotation\"`` or ``\"start-end:rotation\"`` or ``\"start-:rotation\"`` ..."),
                                                )],
    output_file: Annotated[str | None, typer.Option("--output", "-o",
                                                    help=f"{_('Output file')} ({', '.join(PyPDFBackend.SUPPORTED_OUT_FORMATS)}). {_('Defaults to None')} ({_('use the same input file as output name')}, {_('with _rotated.pdf at the end)')}",
                                                    callback=lambda x: check_file_format(x, PyPDFBackend.SUPPORTED_OUT_FORMATS),
                                                    )] = None,
    decrypt_password: Annotated[str | None, typer.Option("--password", "-p",
                                                         help=_("Password used to open protected file. Defaults to None (do not decrypt)."),
                                                         )] = None,
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        rotate_task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None,)

        # get rotation dict in format {page: rotation}
        rotation_dict = {}
        ROTATION_RE = re.compile(r'(\d+)(-(\d*)){0,1}:([-]{0,1}\d+)')
        for arg in rotation:
            match = ROTATION_RE.search(arg)
            if not match:
                raise RuntimeError(f"{_('Invalid rotation instruction')} '{arg}'. {_("Valid format is 'begin-end:degree' or 'page:degree'")}.")

            # check user input
            begin = int(match.group(1)) - 1
            end = begin
            if match.group(3):
                end = int(match.group(3)) - 1
            elif match.group(2):
                end = pypdf_backend.len(input_file)
            degree = int(match.group(4))
            if end < begin:
                raise RuntimeError(f"{_('Invalid begin-end page interval')}. {_('End Page < Begin Page')} '{arg}'.")

            # create rotation_dict
            for page_num in range(begin, end + 1):
                rotation_dict[page_num] = degree

        pypdf_backend.rotate(
            # files
            input_file=input_file,
            output_file=output_file if output_file else f"{input_file.replace(".pdf", "")}_rotated.pdf",

            # passwords
            decrypt_password=decrypt_password,

            # other args
            rotations=rotation_dict,
        )
        progress.update(rotate_task, total=100, completed=100)

    logger.info(f"{_('Rotate pages')}: [bold green]{_('SUCCESS')}[/].")


# pdf encrypt
@pdf_cmd.command(
    rich_help_panel=SECURITY_PANEL,
    help=f"""
        {_('Protect PDF file with a password (create encrypted PDF file).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor pdf encrypt input_file.pdf -o output_file.pdf --owner-password 1234`

        - `file_conversor pdf encrypt input_file.pdf -o output_file.pdf -op 1234 --up 0000 -an -co`
    """)
def encrypt(
    input_file: Annotated[str, typer.Argument(help=f"{_('Input file')} ({', '.join(PyPDFBackend.SUPPORTED_IN_FORMATS)})",
                                              callback=lambda x: check_file_format(x, PyPDFBackend.SUPPORTED_IN_FORMATS, exists=True),
                                              )],
    owner_password: Annotated[str, typer.Option("--owner-password", "-op",
                                                help=_("Owner password for encryption. Owner has ALL PERMISSIONS in the output PDF file."),
                                                prompt=f"{_('Owner password for encryption (password will not be displayed, for your safety)')}",
                                                hide_input=True,
                                                )],

    output_file: Annotated[str | None, typer.Option("--output", "-o",
                                                    help=f"{_('Output file')} ({', '.join(PyPDFBackend.SUPPORTED_OUT_FORMATS)}). {_('Defaults to None')} ({_('use the same input file as output name')}, {_('with _encrypted.pdf at the end)')}",
                                                    callback=lambda x: check_file_format(x, PyPDFBackend.SUPPORTED_OUT_FORMATS),
                                                    )] = None,
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
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        encrypt_task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None,)
        pypdf_backend.encrypt(
            # files
            input_file=input_file,
            output_file=output_file if output_file else f"{input_file.replace(".pdf", "")}_encrypted.pdf",

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
        )
        progress.update(encrypt_task, total=100, completed=100)

    logger.info(f"{_('Encryption')}: [bold green]{_('SUCCESS')}[/].")


# pdf decrypt
@pdf_cmd.command(
    rich_help_panel=SECURITY_PANEL,
    help=f"""
        {_('Remove password protection from a PDF file  (create decrypted PDF file).')}        
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor pdf decrypt input_file.pdf output_file.pdf --password 1234`

        - `file_conversor pdf decrypt input_file.pdf output_file.pdf -p 1234`
    """)
def decrypt(
    input_file: Annotated[str, typer.Argument(help=f"{_('Input file')} ({', '.join(PyPDFBackend.SUPPORTED_IN_FORMATS)})",
                                              callback=lambda x: check_file_format(x, PyPDFBackend.SUPPORTED_IN_FORMATS, exists=True),
                                              )],
    password: Annotated[str, typer.Option("--password", "-p",
                                          help=_("Password used for decryption."),
                                          prompt=f"{_('Password for decryption (password will not be displayed, for your safety)')}",
                                          hide_input=True,
                                          )],

    output_file: Annotated[str | None, typer.Option("--output", "-o",
                                                    help=f"{_('Output file')} ({', '.join(PyPDFBackend.SUPPORTED_OUT_FORMATS)}). {_('Defaults to None')} ({_('use the same input file as output name')}, {_('with _decrypted.pdf at the end)')}",
                                                    callback=lambda x: check_file_format(x, PyPDFBackend.SUPPORTED_OUT_FORMATS),
                                                    )] = None,
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        decrypt_task = progress.add_task(f"{_('Processing file')} '{input_file}':", total=None,)
        pypdf_backend.decrypt(
            input_file=input_file,
            output_file=output_file if output_file else f"{input_file.replace(".pdf", "")}_decrypted.pdf",
            password=password,
        )
        progress.update(decrypt_task, total=100, completed=100)

    logger.info(f"{_('Decryption')}: [bold green]{_('SUCCESS')}[/].")
