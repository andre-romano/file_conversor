# src/backend/pypdf_backend.py

"""
This module provides functionalities for handling PDF files using ``pypdf`` backend.
"""

import math

from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions

from typing import Iterable

# user-provided imports
from config import Log

from backend.abstract_backend import AbstractBackend

LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class PyPDFBackend(AbstractBackend):
    """
    A class that provides an interface for handling PDF files using ``pypdf``.
    """

    SUPPORTED_IN_FORMATS = {
        "pdf": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "pdf": {},
    }

    def __init__(
        self,
        verbose: bool = False,
    ):
        """
        Initialize the ``pypdf`` backend

        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__()
        self._verbose = verbose

    def merge(self,
              output_file: str,
              input_files: dict[str, str],
              ):
        """
        Merge input files into an output.

        ```python
        input_files = {
            file_path_1: password_1,
            file_path_2: password_2,
            ...
        }
        ```

        :param output_file: Output PDF file.
        :param input_files: Input PDF files. Format ``dict[file_path, password]`` (if file not encrypted, use ``password = None``).

        :raises FileNotFoundError: if input file not found.
        """
        output_file = output_file.replace(".pdf", "")

        with PdfWriter() as writer:
            for in_file, decrypt_password in input_files.items():
                self.check_file_exists(in_file)
                with PdfReader(in_file) as reader:
                    if decrypt_password and reader.is_encrypted:
                        reader.decrypt(decrypt_password)
                    for page in reader.pages:
                        writer.add_page(page)
            writer.write(f"{output_file}.pdf")

    def split(self,
              output_file: str,
              input_file: str,
              decrypt_password: str | None = None,
              ):
        """
        Split input files into 1-page PDF output files.

        :param output_file: Output PDF file (will be appended with ``_X.pdf`` where ``X`` is the page number)
        :param input_file: Input PDF file

        :param decrypt_password: Password used to decrypt file, if needed. Defaults to None (do not decrypt).

        :raises FileNotFoundError: if input file not found
        """
        self.check_file_exists(input_file)
        output_file = output_file.replace(".pdf", "")

        with PdfReader(input_file) as reader:
            if decrypt_password and reader.is_encrypted:
                reader.decrypt(decrypt_password)
            for i, page in enumerate(reader.pages):
                with PdfWriter() as writer:
                    writer.add_page(page)
                    writer.write(f"{output_file}_{i + 1}.pdf")

    def extract(self,
                output_file: str,
                input_file: str,
                pages: Iterable[int],
                decrypt_password: str | None = None,
                ):
        """
        Extract specific pages from input files into a PDF output file.

        :param output_file: Output PDF file
        :param input_file: Input PDF file

        :param pages: List of pages to extract (0-indexed).
        :param decrypt_password: Password used to decrypt file, if needed. Defaults to None (do not decrypt).

        :raises FileNotFoundError: if input file not found
        """
        self.check_file_exists(input_file)
        output_file = output_file.replace(".pdf", "")

        with PdfReader(input_file) as reader, PdfWriter() as writer:
            if decrypt_password and reader.is_encrypted:
                reader.decrypt(decrypt_password)

            for page_num in pages:
                writer.add_page(reader.pages[page_num])
            writer.write(f"{output_file}.pdf")

    def rotate(self,
               output_file: str,
               input_file: str,
               rotations: dict[int, int],
               decrypt_password: str | None = None,
               ):
        """
        Rotate specific pages from input files, generating a PDF output file.

        :param output_file: Output PDF file.
        :param input_file: Input PDF file.

        :param rotations: Dict format { page_num: rotation_degrees }. Degree must be 0 or multiples of 90 degrees - positive or negative.
        :param decrypt_password: Password used to decrypt file, if needed. Defaults to None (do not decrypt).

        :raises FileNotFoundError: if input file not found
        :raises ValueError: if rotation degree is invalid (valid values are 0 or multiples of 90 degrees - positive or negative).        
        """
        self.check_file_exists(input_file)
        output_file = output_file.replace(".pdf", "")

        with PdfReader(input_file) as reader, PdfWriter() as writer:
            if decrypt_password and reader.is_encrypted:
                reader.decrypt(decrypt_password)

            for i, page in enumerate(reader.pages):
                rotation = int(rotations.get(i, 0))

                # parse rotation argument
                rotation = int(math.fmod(rotation, 360))
                if rotation < 0:
                    rotation += 360  # fix rotation signal

                if rotation not in (0, 90, 180, 270):
                    raise ValueError(f"Page '{i}' rotation {rotation} is invalid. Rotation must be 0, 90, 180 or 270 degrees.")

                # execute page rotation
                logger.debug(f"Instruction: {i} {rotation}")
                if rotation > 0:
                    page.rotate(rotation)  # clockwise: 90, 180, 270
                writer.add_page(page)
            # save output file
            writer.write(f"{output_file}.pdf")

    def encrypt(self,
                output_file: str,
                input_file: str,
                owner_password: str,
                user_password: str | None = None,
                decrypt_password: str | None = None,
                permission_annotate: bool = False,
                permission_fill_forms: bool = False,
                permission_modify: bool = False,
                permission_modify_pages: bool = False,
                permission_copy: bool = False,
                permission_accessibility: bool = True,
                permission_print_low_quality: bool = True,
                permission_print_high_quality: bool = True,
                permission_all: bool = False,
                encryption_algorithm: str = "AES-256",
                ):
        """
        Encrypt input file, generating a protected PDF output file.

        **Available permissions:**
        - ``permission_annotate``: User can add/modify annotations (comments, highlight text, etc) and interactive forms. Default to False (not set).
        - ``permission_fill_forms``: User can fill form fields (subset permission of `permission_annotate`). Default to False (not set).
        - ``permission_modify``: User can modify the document (e.g., add / edit text, add / edit images, etc). Default to False (not set).
        - ``permission_modify_pages``: User can insert, delete, or rotate pages (subset of ``permission_modify``). Default to False (not set).
        - ``permission_copy``: User can copy text/images. Default to False (not set).
        - ``permission_accessibility``: User can use screen readers for accessibility. Default to True (not set).
        - ``permission_print_low_quality``: User can PRINT pdf (low quality). Defaults to True (allow).
        - ``permission_print_high_quality``: User can PRINT pdf (high quality). Requires `permission_print_low_quality=True`. Defaults to True (allow).
        - ``permission_all``: User has ALL PERMISSIONS. If True, it overrides all other permissions. Defaults to False (not set).

        **Encryption algorithms:**
        - ``AES-256``    (high security, compatible with 2008+ PDF readers - **RECOMMENDED**)
        - ``AES-128``    (good security, good compatibility - **RECOMMENDED**)
        - ``AES-256-R5`` (high security,  lowest compatibility - not recommended)
        - ``RC4-128``    (weak security, highest compatibility - not recommended)
        - ``RC4-40``     (weakest security - not recommended)

        :param output_file: Output PDF file.
        :param input_file: Input PDF file.

        :param owner_password: Owner password for encryption. Owner has ALL PERMISSIONS in the output PDF file.
        :param user_password:  User password for encryption. User has ONLY THE PERMISSIONS specified in the arguments. Defaults to None (user and owner password are the same).
        :param decrypt_password: Password used to decrypt file, if needed. Defaults to None (do not decrypt).

        :param permission_annotate: User can add/modify annotations (comments, highlight text, etc) and interactive forms. Default to False (not set).
        :param permission_fill_forms: User can fill form fields (subset permission of `permission_annotate`). Default to False (not set).
        :param permission_modify: User can modify the document (e.g., add / edit text, add / edit images, etc). Default to False (not set).
        :param permission_modify_pages: User can insert, delete, or rotate pages (subset of ``permission_modify``). Default to False (not set).
        :param permission_copy: User can copy text/images. Default to False (not set).
        :param permission_accessibility: User can use screen readers for accessibility. Default to True (allow).
        :param permission_print_low_quality: User can PRINT pdf (low quality). Defaults to True (allow).
        :param permission_print_high_quality: User can PRINT pdf (high quality). Requires `permission_print_low_quality=True`. Defaults to True (allow).
        :param permission_all: User has ALL PERMISSIONS. If True, it overrides all other permissions. Defaults to False (not set).

        :param encryption_algorithm: Encryption algorithm used. Valid options are "RC4-40", "RC4-128", "AES-128", "AES-256-R5", or "AES-256". Defaults to "AES-256" (for enhanced security and compatibility).

        :raises FileNotFoundError: if input file not found
        """
        self.check_file_exists(input_file)
        output_file = output_file.replace(".pdf", "")

        with PdfReader(input_file) as reader, PdfWriter() as writer:
            if decrypt_password and reader.is_encrypted:
                reader.decrypt(decrypt_password)

            if encryption_algorithm not in (None, "RC4-40", "RC4-128", "AES-128", "AES-256-R5", "AES-256"):
                raise ValueError(f"Encryption algorithm '{encryption_algorithm}' is invalid.  Valid options are 'RC4-40', 'RC4-128', 'AES-128', 'AES-256-R5', or 'AES-256'.")

            # set user permissions
            permissions = UserAccessPermissions(0)
            if permission_annotate:
                permissions |= UserAccessPermissions.ADD_OR_MODIFY
            if permission_fill_forms:
                permissions |= UserAccessPermissions.FILL_FORM_FIELDS
            if permission_modify:
                permissions |= UserAccessPermissions.MODIFY
            if permission_modify_pages:
                permissions |= UserAccessPermissions.ASSEMBLE_DOC
            if permission_copy:
                permissions |= UserAccessPermissions.EXTRACT
            if permission_accessibility:
                permissions |= UserAccessPermissions.EXTRACT_TEXT_AND_GRAPHICS
            if permission_print_low_quality:
                permissions |= UserAccessPermissions.PRINT
            if permission_print_high_quality:
                permissions |= UserAccessPermissions.PRINT_TO_REPRESENTATION
            if permission_all:
                permissions |= UserAccessPermissions.all()

            # add pages into writer
            for page in reader.pages:
                writer.add_page(page)

            # Encrypt with user and owner passwords
            writer.encrypt(
                owner_password=owner_password,
                user_password=user_password if user_password else owner_password,
                permissions_flag=permissions,
                algorithm=encryption_algorithm,
                use_128bit=True,
            )

            # save output file
            writer.write(f"{output_file}.pdf")

    def decrypt(self,
                output_file: str,
                input_file: str,
                password: str,
                ):
        """
        Decrypt input file, generating a non-protected PDF output file.

        :param output_file: Output PDF file.
        :param input_file: Input PDF file.

        :param password: Password used to decrypt file.

        :raises FileNotFoundError: if input file not found
        """
        self.check_file_exists(input_file)
        output_file = output_file.replace(".pdf", "")

        with PdfReader(input_file) as reader, PdfWriter() as writer:
            # decrypt file
            if reader.is_encrypted:
                reader.decrypt(password)

            # Generate decrypted pdf
            for page in reader.pages:
                writer.add_page(page)
            writer.write(f"{output_file}.pdf")
