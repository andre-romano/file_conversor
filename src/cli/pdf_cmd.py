
# src\cli\pdf_cmd.py

import re
import time
import typer

from typing import Annotated, List

from rich import print

# user-provided modules
from backend import PyPDFBackend, QPDFBackend

from config import Configuration, State
from config.locale import get_translation

from utils.rich import get_progress_bar
from utils.validators import check_file_format, check_pdf_encrypt_algorithm
from utils.formatters import YES_ICON

# get app config
_ = get_translation()
CONFIG = Configuration.get_instance()
STATE = State.get_instance()

# typer PANELS
SECURITY_PANEL = _(f"Security commands")

pdf_cmd = typer.Typer()


# pdf repair
@pdf_cmd.command(
    help=f"""
        {_('Repair (lightly) corrupted PDF files (requires QPDF external library).')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor pdf repair input_file.pdf output_file.pdf` 
""")
def repair(
    input_file: Annotated[str, typer.Argument(help=_("Input file path"),
                                              callback=lambda x: check_file_format(x, ['pdf'], exists=True),
                                              )],
    output_file: Annotated[str | None, typer.Argument(help=f"{_('Output file path')}. Defaults to None (use the same input file as output name).",
                                                      callback=lambda x: check_file_format(x, ['pdf']),
                                                      )] = None,
    decrypt_password: Annotated[str | None, typer.Option("--password", "-p",
                                                         help=_("Password used to open protected file. Defaults to None (do not decrypt)."),
                                                         )] = None,
):
    qpdf_backend = QPDFBackend(verbose=STATE["verbose"], install_deps=CONFIG['install-deps'])
    with get_progress_bar() as progress:
        task1 = progress.add_task(f"{_('Repairing PDF')} ...", total=None,)

        process = qpdf_backend.repair(
            # files
            input_file=input_file,
            output_file=output_file if output_file else f"{input_file.replace(".pdf", "")}_repaired.pdf",

            # passwords
            decrypt_password=decrypt_password,
        )
        while process.poll() is None:
            time.sleep(0.25)
        progress.update(task1, total=100, completed=100)

    process.wait()
    if process.returncode != 0:
        raise RuntimeError(qpdf_backend.dump_streams(process))

    print(f"--------------------------------")
    print(f"{_('Repair PDF')}: [bold green]{_('SUCCESS')}[/] {YES_ICON}.")
    print(f"--------------------------------")


# pdf merge
@pdf_cmd.command(
    help=f"""
        {_('Merge (join) input PDFs into a single PDF file.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Merge files "input_file1.pdf" and "input_file2.pdf" into "output_file.pdf"')}*:

- `file_conversor pdf merge "input_file1.pdf" "input_file2.pdf" output_file.pdf` 



*{_('Merge protected PDF "input_file1.pdf" with password "unlock_password" with unprotected file "input_file2.pdf"')}*:

- `file_conversor pdf merge "input_file1.pdf:unlock_password" "input_file2.pdf" output_file.pdf` 
    """)
def merge(
    input_files: Annotated[List[str], typer.Argument(help=f"{_('Input file path')}. {_('If file is protected, provide its password using the format `"filepath:password"`')}.",
                                                     )],
    output_file: Annotated[str, typer.Argument(help=_("Output file path"),
                                               callback=lambda x: check_file_format(x, ['pdf']),
                                               )],
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        merge_task = progress.add_task(f"{_('Merging PDFs')} ...", total=None,)

        # get dict in format {filepath: password}
        filepath_dict = {}
        FILEPATH_RE = re.compile(r'^(.+?)(::(.+))?$')
        for arg in input_files:
            match = FILEPATH_RE.search(arg)
            if not match:
                raise RuntimeError(f"{_('Invalid filepath format')} '{arg}'. {_("Valid format is 'filepath:password' or 'filepath'")}.")

            # check user input
            filepath = check_file_format(match.group(1), ['pdf'], exists=True)
            password = match.group(3) if match.group(3) else None

            # create filepath_dict
            filepath_dict[filepath] = password

        pypdf_backend.merge(
            # files
            input_files=filepath_dict,
            output_file=output_file,
        )
        progress.update(merge_task, total=100, completed=100)

    print(f"--------------------------------")
    print(f"{_('Merge pages')}: [bold green]{_('SUCCESS')}[/] {YES_ICON}.")
    print(f"--------------------------------")


# pdf split
@pdf_cmd.command(
    help=f"""
        {_('Split PDF pages into several 1-page PDFs.')}

        {_('For every PDF page, a new single page PDF will be created using the format `output_file_X.pdf`, where X is the page number.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Split pages of input_file.pdf into output_file_X.pdf files')}*:

- `file_conversor pdf split input_file.pdf output_file.pdf` 



*{_('For every PDF page, generate a "input_file_X.pdf" file')}*:

- `file_conversor pdf split input_file.pdf` 
""")
def split(
    input_file: Annotated[str, typer.Argument(help=_("Input file path"),
                                              callback=lambda x: check_file_format(x, ['pdf'], exists=True),
                                              )],
    output_file: Annotated[str | None, typer.Argument(help=f"{_('Output file path')}. Defaults to None (use the same input file as output name).",
                                                      callback=lambda x: check_file_format(x, ['pdf']),
                                                      )] = None,
    decrypt_password: Annotated[str | None, typer.Option("--password", "-p",
                                                         help=_("Password used to open protected file. Defaults to None (do not decrypt)."),
                                                         )] = None,
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        split_task = progress.add_task(f"{_('Splitting pages')} ...", total=None,)

        pypdf_backend.split(
            # files
            input_file=input_file,
            output_file=output_file if output_file else input_file,

            # passwords
            decrypt_password=decrypt_password,
        )
        progress.update(split_task, total=100, completed=100)

    print(f"--------------------------------")
    print(f"{_('Split pages')}: [bold green]{_('SUCCESS')}[/] {YES_ICON}.")
    print(f"--------------------------------")


# pdf extract
@pdf_cmd.command(
    help=f"""
        {_('Extract specific pages from a PDF.')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Extract pages 1-2 and 3')}*:

- `file_conversor pdf extract input_file.pdf output_file.pdf 1-2 3` 
    """)
def extract(
    input_file: Annotated[str, typer.Argument(help=_("Input file path"),
                                              callback=lambda x: check_file_format(x, ['pdf'], exists=True),
                                              )],
    output_file: Annotated[str, typer.Argument(help=_("Output file path"),
                                               callback=lambda x: check_file_format(x, ['pdf']),
                                               )],
    pages: Annotated[List[str], typer.Argument(help=_("List of pages to extract. Format page_num1 page_num2 ..."),
                                               )],
    decrypt_password: Annotated[str | None, typer.Option("--password", "-p",
                                                         help=_("Password used to open protected file. Defaults to None (do not decrypt)."),
                                                         )] = None,
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        extract_task = progress.add_task(f"{_('Extracting pages')} ...", total=None,)

        # parse user input
        pages_list = []
        PAGES_RE = re.compile(r'(\d+)(-(\d+)){0,1}')
        for arg in pages:
            match = PAGES_RE.search(arg)
            if not match:
                raise RuntimeError(f"{_('Invalid page instruction')} '{arg}'. {_("Valid format is 'begin-end' or 'page_num'")}.")

            # check user input
            begin = int(match.group(1)) - 1
            end = int(match.group(3)) - 1 if match.group(3) else begin
            if end < begin:
                raise RuntimeError(f"{_('Invalid begin-end page interval')}. {_('End Page < Begin Page')} '{arg}'.")

            # create rotation_dict
            for page_num in range(begin, end + 1):
                pages_list.append(page_num)

        pypdf_backend.extract(
            # files
            input_file=input_file,
            output_file=output_file,

            # passwords
            decrypt_password=decrypt_password,

            # other args
            pages=pages_list
        )
        progress.update(extract_task, total=100, completed=100)

    print(f"--------------------------------")
    print(f"{_('Extract pages')}: [bold green]{_('SUCCESS')}[/] {YES_ICON}.")
    print(f"--------------------------------")


# pdf rotate
@pdf_cmd.command(
    help=f"""
        {_('Rotate PDF pages (clockwise or anti-clockwise).')}
    """,
    epilog=f"""
**{_('Examples')}:** 



*{_('Rotate page 1 by 180 degress')}*:

- `file_conversor pdf rotate input_file.pdf output_file.pdf "1:180"` 



*{_('Rotate page 5-7 by 90 degress, 9 by -90 degrees, 10-15 by 180 degrees')}*:

- `file_conversor pdf rotate input_file.pdf output_file.pdf "5-7:90" "9:-90" "10-15:180"`
    """)
def rotate(
    input_file: Annotated[str, typer.Argument(help=_("Input file path"),
                                              callback=lambda x: check_file_format(x, ['pdf'], exists=True),
                                              )],
    output_file: Annotated[str, typer.Argument(help=_("Output file path"),
                                               callback=lambda x: check_file_format(x, ['pdf']),
                                               )],
    rotation: Annotated[List[str], typer.Argument(help=_("List of pages to rotate. Format ``\"page1:rotation1\"`` ``\"page2:rotation2\"`` ..."),
                                                  )],
    decrypt_password: Annotated[str | None, typer.Option("--password", "-p",
                                                         help=_("Password used to open protected file. Defaults to None (do not decrypt)."),
                                                         )] = None,
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        rotate_task = progress.add_task(f"{_('Rotating pages')} ...", total=None,)

        # get rotation dict in format {page: rotation}
        rotation_dict = {}
        ROTATION_RE = re.compile(r'(\d+)(-(\d+)){0,1}:([-]{0,1}\d+)')
        for arg in rotation:
            match = ROTATION_RE.search(arg)
            if not match:
                raise RuntimeError(f"{_('Invalid rotation instruction')} '{arg}'. {_("Valid format is 'begin-end:degree' or 'page:degree'")}.")

            # check user input
            begin = int(match.group(1)) - 1
            end = int(match.group(3)) - 1 if match.group(3) else begin
            degree = int(match.group(4))
            if end < begin:
                raise RuntimeError(f"{_('Invalid begin-end page interval')}. {_('End Page < Begin Page')} '{arg}'.")

            # create rotation_dict
            for page_num in range(begin, end + 1):
                rotation_dict[page_num] = degree

        pypdf_backend.rotate(
            # files
            input_file=input_file,
            output_file=output_file,

            # passwords
            decrypt_password=decrypt_password,

            # other args
            rotations=rotation_dict,
        )
        progress.update(rotate_task, total=100, completed=100)

    print(f"--------------------------------")
    print(f"{_('Rotate pages')}: [bold green]{_('SUCCESS')}[/] {YES_ICON}.")
    print(f"--------------------------------")


# pdf encrypt
@pdf_cmd.command(
    rich_help_panel=SECURITY_PANEL,
    help=f"""
        {_('Protect PDF file with a password (create encrypted PDF file).')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor pdf encrypt input_file.pdf output_file.pdf --owner-password 1234`

        - `file_conversor pdf encrypt input_file.pdf output_file.pdf -op 1234 --up 0000 -an -co`
    """)
def encrypt(
    input_file: Annotated[str, typer.Argument(help=_("Input file path"),
                                              callback=lambda x: check_file_format(x, ['pdf'], exists=True),
                                              )],
    output_file: Annotated[str, typer.Argument(help=_("Output file path"),
                                               callback=lambda x: check_file_format(x, ['pdf']),
                                               )],

    owner_password: Annotated[str, typer.Option("--owner-password", "-op",
                                                help=_("Owner password for encryption. Owner has ALL PERMISSIONS in the output PDF file."),
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
                                              callback=check_pdf_encrypt_algorithm
                                              )] = "AES-256",
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        encrypt_task = progress.add_task(f"{_('Encripting file')} ...", total=None,)
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
        )
        progress.update(encrypt_task, total=100, completed=100)

    print(f"--------------------------------")
    print(f"{_('Encryption')}: [bold green]{_('SUCCESS')}[/] {YES_ICON}.")
    print(f"--------------------------------")


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
    input_file: Annotated[str, typer.Argument(help=_("Input file path"),
                                              callback=lambda x: check_file_format(x, ['pdf'], exists=True),
                                              )],
    output_file: Annotated[str, typer.Argument(help=_("Output file path"),
                                               callback=lambda x: check_file_format(x, ['pdf']),
                                               )],

    password: Annotated[str, typer.Option("--password", "-p",
                                          help=_("Password used for decryption."),
                                          )],
):
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])
    with get_progress_bar() as progress:
        decrypt_task = progress.add_task(f"{_('Decripting file')} ...", total=None,)
        pypdf_backend.decrypt(
            input_file=input_file,
            output_file=output_file,
            password=password,
        )
        progress.update(decrypt_task, total=100, completed=100)

    print(f"--------------------------------")
    print(f"{_('Decryption')}: [bold green]{_('SUCCESS')}[/] {YES_ICON}.")
    print(f"--------------------------------")
