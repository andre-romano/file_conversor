# src\file_conversor\backend\pypdf_backend.py

"""
This module provides functionalities for handling PDF files using ``pypdf`` backend.
"""

from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions

from enum import Enum
from pathlib import Path

from typing import Any, Callable, Iterable, Sequence

# user-provided imports
from file_conversor.config import Log

from file_conversor.utils.formatters import normalize_degree

from file_conversor.backend.abstract_backend import AbstractBackend

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
    EXTERNAL_DEPENDENCIES: set[str] = set()

    class EncryptionPermission(Enum):
        NONE = 'none'
        """ No permissions granted to user (read-only) """

        ANNOTATE = 'annotate'
        """ User can add/modify annotations (comments, highlight text, etc) and interactive forms. """

        FILL_FORMS = 'fill_forms'
        """ User can fill interactive form fields. """

        MODIFY = 'modify'
        """ User can modify the document (except pages). """

        MODIFY_PAGES = 'modify_pages'
        """ User can modify the document's pages (insert, delete, rotate, etc). """

        COPY = 'copy'
        """ User can copy text and graphics from the document. """

        ACCESSIBILITY = 'accessibility'
        """ User can extract text and graphics for accessibility purposes. """

        PRINT_LQ = 'print_lq'
        """ User can print the document in low quality. """

        PRINT_HQ = 'print_hq'
        """ User can print the document in high quality. """

        ALL = 'all'
        """ All permissions granted to user. """

        def get_value(self):
            """Get permission value."""
            return {
                'none': UserAccessPermissions(0),
                'annotate': UserAccessPermissions.ADD_OR_MODIFY,
                'fill_forms': UserAccessPermissions.FILL_FORM_FIELDS,
                'modify': UserAccessPermissions.MODIFY,
                'modify_pages': UserAccessPermissions.ASSEMBLE_DOC,
                'copy': UserAccessPermissions.EXTRACT,
                'accessibility': UserAccessPermissions.EXTRACT_TEXT_AND_GRAPHICS,
                'print_lq': UserAccessPermissions.PRINT,
                'print_hq': UserAccessPermissions.PRINT_TO_REPRESENTATION,
                'all': UserAccessPermissions.all(),
            }[self.value]

        @classmethod
        def get_dict(cls) -> dict[str, 'PyPDFBackend.EncryptionPermission']:
            """Get dictionary of encryption algorithms."""
            return dict(cls.__members__)

        @classmethod
        def from_str(cls, name: str):
            """Get encryption algorithm from string."""
            name = name.upper()
            alg_dict = cls.get_dict()
            if name not in alg_dict:
                raise ValueError(f"Encryption permission '{name}' is invalid. Valid options are: {', '.join(alg_dict.keys())}.")
            return alg_dict[name]

    class EncryptionAlgorithm(Enum):
        """PDF encryption algorithms."""

        AES_256 = "AES-256"
        AES_256_R5 = "AES-256-R5"
        AES_128 = "AES-128"
        RC4_128 = "RC4-128"
        RC4_40 = "RC4-40"

        @classmethod
        def get_dict(cls):
            """Get dictionary of encryption algorithms."""
            return {
                "AES-256": PyPDFBackend.EncryptionAlgorithm.AES_256,
                "AES-256-R5": PyPDFBackend.EncryptionAlgorithm.AES_256_R5,
                "AES-128": PyPDFBackend.EncryptionAlgorithm.AES_128,
                "RC4-128": PyPDFBackend.EncryptionAlgorithm.RC4_128,
                "RC4-40": PyPDFBackend.EncryptionAlgorithm.RC4_40,
            }

        @classmethod
        def from_str(cls, name: str):
            """Get encryption algorithm from string."""
            alg_dict = cls.get_dict()
            if name not in alg_dict:
                raise ValueError(f"Encryption algorithm '{name}' is invalid. Valid options are: {', '.join(alg_dict.keys())}.")
            return alg_dict[name]

    @staticmethod
    def len(
            input_file: str | Path,
    ) -> int:
        """
        Get number of pages of input file.

        :param input_file: Input PDF file.

        :return: Number of pages.

        :raises FileNotFoundError: if input file not found
        """
        PyPDFBackend.check_file_exists(input_file)

        with PdfReader(input_file) as reader:
            return len(reader.pages)

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
              output_file: str | Path,
              input_files: Sequence[str | Path],
              password: str | None = None,
              progress_callback: Callable[[float], Any] | None = None,
              ):
        """
        Merge input files into an output.

        :param output_file: Output PDF file.
        :param input_files: Input PDF files. 
        :param password: Decryption password. Defaults to None.
        :param progress_callback: Progress callback (0-100). Defaults to None.

        :raises FileNotFoundError: if input file not found.
        """
        output_file = Path(output_file).with_suffix(".pdf")
        completed = 0.0
        file_progress = 100.0 / len(input_files)

        with PdfWriter() as writer:
            for idx, input_file in enumerate(input_files, start=1):
                input_file = Path(input_file)
                self.check_file_exists(input_file)

                with PdfReader(input_file) as reader:
                    if password and reader.is_encrypted:
                        reader.decrypt(password)

                    pages_len = len(reader.pages)
                    for page in reader.pages:
                        writer.add_page(page)

                        completed += file_progress / pages_len
                        if progress_callback:
                            progress_callback(completed)
            if progress_callback:
                progress_callback(100.0)
            writer.write(output_file)

    def split(self,
              output_file: str | Path,
              input_file: str | Path,
              password: str | None = None,
              progress_callback: Callable[[float], Any] | None = None,
              ):
        """
        Split input files into 1-page PDF output files.

        :param output_file: Output PDF file (will be appended with ``_X.pdf`` where ``X`` is the page number)
        :param input_file: Input PDF file
        :param password: Decryption password. Defaults to None.
        :param progress_callback: Progress callback (0-100). Defaults to None.

        :raises FileNotFoundError: if input file not found
        """
        self.check_file_exists(input_file)
        output_path = Path(output_file).with_suffix("")

        with PdfReader(input_file) as reader:
            if password and reader.is_encrypted:
                reader.decrypt(password)

            pages_len = len(reader.pages)
            for i, page in enumerate(reader.pages):
                with PdfWriter() as writer:
                    writer.add_page(page)
                    writer.write(f"{output_path}_{i + 1}.pdf")

                    progress = 100.0 * (float(i) / pages_len)
                    if progress_callback:
                        progress_callback(progress)

    def extract(self,
                output_file: str | Path,
                input_file: str | Path,
                pages: Sequence[int],
                password: str | None = None,
                progress_callback: Callable[[float], Any] | None = None,
                ):
        """
        Extract specific pages from input files into a PDF output file.

        :param output_file: Output PDF file
        :param input_file: Input PDF file
        :param pages: List of pages to extract (0-indexed).
        :param password: Password used to decrypt file, if needed. Defaults to None (do not decrypt).
        :param progress_callback: Progress callback (0-100). Defaults to None.

        :raises FileNotFoundError: if input file not found
        """
        self.check_file_exists(input_file)
        output_path = Path(output_file).with_suffix(".pdf")

        with PdfReader(input_file) as reader, PdfWriter() as writer:
            if password and reader.is_encrypted:
                reader.decrypt(password)

            pdf_len = len(reader.pages)
            pages_len = len(pages)
            for idx, page_num in enumerate(pages, start=1):
                if pdf_len <= page_num:
                    raise ValueError(f"PDF '{input_file}' has only {len(reader.pages)} pages. Cannot extract page {page_num + 1}.")
                writer.add_page(reader.pages[page_num])

                progress = 100.0 * (float(idx) / pages_len)
                if progress_callback:
                    progress_callback(progress)
            if progress_callback:
                progress_callback(100.0)
            writer.write(output_path)

    def rotate(self,
               output_file: str | Path,
               input_file: str | Path,
               rotations: dict[int, int],
               decrypt_password: str | None = None,
               progress_callback: Callable[[float], Any] | None = None,
               ):
        """
        Rotate specific pages from input files, generating a PDF output file.

        :param output_file: Output PDF file.
        :param input_file: Input PDF file.
        :param rotations: Dict format { page_num: rotation_degrees }. Degree must be 0 or multiples of 90 degrees - positive or negative.
        :param decrypt_password: Password used to decrypt file, if needed. Defaults to None (do not decrypt).
        :param progress_callback: Progress callback (0-100). Defaults to None.

        :raises FileNotFoundError: if input file not found
        :raises ValueError: if rotation degree is invalid (valid values are 0 or multiples of 90 degrees - positive or negative).        
        """
        self.check_file_exists(input_file)
        output_path = Path(output_file).with_suffix(".pdf")

        with PdfReader(input_file) as reader, PdfWriter() as writer:
            if decrypt_password and reader.is_encrypted:
                reader.decrypt(decrypt_password)

            pages_len = len(reader.pages)
            for i, page in enumerate(reader.pages):
                rotation = int(rotations.get(i, 0))

                # parse rotation argument
                rotation = normalize_degree(rotation)

                if rotation not in (0, 90, 180, 270):
                    raise ValueError(f"Page '{i}' rotation {rotation} is invalid. Rotation must be 0, 90, 180 or 270 degrees.")

                # execute page rotation
                logger.debug(f"Rotating page {i} by {rotation} deg")
                if rotation > 0:
                    page.rotate(rotation)  # clockwise: 90, 180, 270
                writer.add_page(page)

                progress = 100.0 * (float(i) / pages_len)
                if progress_callback:
                    progress_callback(progress)

            if progress_callback:
                progress_callback(100.0)
            # save output file
            writer.write(output_path)

    def encrypt(self,
                output_file: str | Path,
                input_file: str | Path,
                owner_password: str,
                user_password: str | None = None,
                decrypt_password: str | None = None,
                permissions: Iterable[EncryptionPermission] | None = None,
                encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.AES_256,
                progress_callback: Callable[[float], Any] | None = None,
                ):
        """
        Encrypt input file, generating a protected PDF output file.

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

        :param permissions: List of permissions to grant to the user. If None, no permissions are granted (user can only open the file). Format: [``EncryptionPermission.ANNOTATE``, ``EncryptionPermission.PRINT_LOW_QUALITY``, ...]. Defaults to None.

        :param encryption_algorithm: Encryption algorithm used. Defaults to "AES-256" (for enhanced security and compatibility).
        :param progress_callback: Progress callback (0-100). Defaults to None.

        :raises FileNotFoundError: if input file not found
        """
        self.check_file_exists(input_file)
        output_path = Path(output_file).with_suffix(".pdf")

        with PdfReader(input_file) as reader, PdfWriter() as writer:
            if decrypt_password and reader.is_encrypted:
                reader.decrypt(decrypt_password)

            # set user permissions
            permissions_flag = PyPDFBackend.EncryptionPermission.NONE.get_value()
            for perm in permissions or []:
                permissions_flag |= perm.get_value()

            # add pages into writer
            pages_len = len(reader.pages)
            for i, page in enumerate(reader.pages, start=0):
                writer.add_page(page)
                progress = 100.0 * (float(i) / pages_len)
                if progress_callback:
                    progress_callback(progress)

            # Encrypt with user and owner passwords
            writer.encrypt(
                owner_password=owner_password,
                user_password=user_password if user_password else owner_password,
                permissions_flag=permissions_flag,
                algorithm=encryption_algorithm.value,
                use_128bit=True,
            )

            # save output file
            writer.write(output_path)

            if progress_callback:
                progress_callback(100.0)

    def decrypt(self,
                output_file: str | Path,
                input_file: str | Path,
                password: str,
                progress_callback: Callable[[float], Any] | None = None,
                ):
        """
        Decrypt input file, generating a non-protected PDF output file.

        :param output_file: Output PDF file.
        :param input_file: Input PDF file.
        :param password: Password used to decrypt file.
        :param progress_callback: Progress callback (0-100). Defaults to None.

        :raises FileNotFoundError: if input file not found
        """
        self.check_file_exists(input_file)
        output_path = Path(output_file).with_suffix(".pdf")

        with PdfReader(input_file) as reader, PdfWriter() as writer:
            # decrypt file
            if reader.is_encrypted:
                reader.decrypt(password)

            # Generate decrypted pdf
            pages_len = len(reader.pages)
            for i, page in enumerate(reader.pages, start=0):
                writer.add_page(page)
                progress = 100.0 * (float(i) / pages_len)
                if progress_callback:
                    progress_callback(progress)

            # save file
            writer.write(output_path)
            if progress_callback:
                progress_callback(100.0)


__all__ = [
    "PyPDFBackend",
]
