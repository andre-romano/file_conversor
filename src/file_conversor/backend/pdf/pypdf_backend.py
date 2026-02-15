# src\file_conversor\backend\pypdf_backend.py

"""
This module provides functionalities for handling PDF files using ``pypdf`` backend.
"""

from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions

from file_conversor.backend.abstract_backend import AbstractBackend

# user-provided imports
from file_conversor.config import Log, get_translation


_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class PyPDFBackend(AbstractBackend):
    """
    A class that provides an interface for handling PDF files using ``pypdf``.
    """
    class Rotation(Enum):
        """Rotation degrees for PDF page rotation."""
        DEG_0 = 0
        DEG_90 = 90
        DEG_180 = 180
        DEG_270 = 270

    class SupportedInFormats(Enum):
        PDF = "pdf"

    class SupportedOutFormats(Enum):
        PDF = "pdf"

    EXTERNAL_DEPENDENCIES: set[str] = set()

    class EncryptionPermission(Enum):
        """PDF user access permissions."""

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

        def get(self) -> UserAccessPermissions:
            """Get permission value."""
            match self:
                case PyPDFBackend.EncryptionPermission.NONE:
                    return UserAccessPermissions(0)
                case PyPDFBackend.EncryptionPermission.ANNOTATE:
                    return UserAccessPermissions.ADD_OR_MODIFY
                case PyPDFBackend.EncryptionPermission.FILL_FORMS:
                    return UserAccessPermissions.FILL_FORM_FIELDS
                case PyPDFBackend.EncryptionPermission.MODIFY:
                    return UserAccessPermissions.MODIFY
                case PyPDFBackend.EncryptionPermission.MODIFY_PAGES:
                    return UserAccessPermissions.ASSEMBLE_DOC
                case PyPDFBackend.EncryptionPermission.COPY:
                    return UserAccessPermissions.EXTRACT
                case PyPDFBackend.EncryptionPermission.ACCESSIBILITY:
                    return UserAccessPermissions.EXTRACT_TEXT_AND_GRAPHICS
                case PyPDFBackend.EncryptionPermission.PRINT_LQ:
                    return UserAccessPermissions.PRINT
                case PyPDFBackend.EncryptionPermission.PRINT_HQ:
                    return UserAccessPermissions.PRINT_TO_REPRESENTATION
                case PyPDFBackend.EncryptionPermission.ALL:
                    return UserAccessPermissions.all()

    class EncryptionAlgorithm(Enum):
        """PDF encryption algorithms."""

        AES_256 = "aes-256"
        AES_256_R5 = "aes-256-r5"
        AES_128 = "aes-128"
        RC4_128 = "rc4-128"
        RC4_40 = "rc4-40"

        def get(self) -> str:
            """Get algorithm value."""
            match self:
                case PyPDFBackend.EncryptionAlgorithm.AES_256:
                    return "AES-256"
                case PyPDFBackend.EncryptionAlgorithm.AES_256_R5:
                    return "AES-256-R5"
                case PyPDFBackend.EncryptionAlgorithm.AES_128:
                    return "AES-128"
                case PyPDFBackend.EncryptionAlgorithm.RC4_128:
                    return "RC4-128"
                case PyPDFBackend.EncryptionAlgorithm.RC4_40:
                    return "RC4-40"

    @staticmethod
    def len(input_file: Path) -> int:
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

    def _merge(self,
               input_file: Path,
               writer: PdfWriter,
               password: str = "",
               progress_callback: Callable[[float], Any] = lambda p: p,
               ):
        """ Merge input file into a PdfWriter. """
        with PdfReader(input_file) as reader:
            if password and reader.is_encrypted:
                reader.decrypt(password)

            pages_len = len(reader.pages)
            for i, page in enumerate(reader.pages, start=1):
                writer.add_page(page)
                progress_callback(i * 100.0 / pages_len)

    def merge(self,
              output_file: Path,
              input_files: Sequence[Path],
              password: str = "",
              progress_callback: Callable[[float], Any] = lambda p: p,
              ):
        """
        Merge input files into an output.

        :param output_file: Output PDF file.
        :param input_files: Input PDF files. 
        :param password: Decryption password. Defaults to "".
        :param progress_callback: Progress callback (0-100). Defaults to a no-op.

        :raises FileNotFoundError: if input file not found.
        """
        completed = 0.0
        file_progress = 100.0 / len(input_files)

        with PdfWriter() as writer:
            for _, input_file in enumerate(input_files, start=1):
                self._merge(
                    input_file=input_file,
                    writer=writer,
                    password=password,
                    progress_callback=lambda p, completed=completed: progress_callback(completed + (p * file_progress / 100.0)),
                )
                completed += file_progress
            writer.write(output_file)
            progress_callback(100.0)

    def split(self,
              input_file: Path,
              overwrite_output: bool,
              password: str = "",
              out_dir: Path = Path(),
              progress_callback: Callable[[float], Any] = lambda p: p,
              ):
        """
        Split input files into 1-page PDF output files.

        :param input_file: Input PDF file (Output PDF file = input + ``_X.pdf`` where ``X`` is the page number)
        :param overwrite_output: Whether to overwrite existing output files.
        :param password: Decryption password. Defaults to "".
        :param progress_callback: Progress callback (0-100). Defaults to a no-op.

        :raises FileNotFoundError: if input file not found
        """
        output_path = out_dir / input_file.with_suffix("").name

        with PdfReader(input_file) as reader:
            if password and reader.is_encrypted:
                reader.decrypt(password)

            pages_len = len(reader.pages)
            for idx, page in enumerate(reader.pages, start=1):
                output_file = Path(f"{output_path}_{idx}.pdf")
                if not overwrite_output and output_file.exists():
                    raise FileExistsError(f"{_('File')} '{output_file}' {_('exists')}")

                with PdfWriter() as writer:
                    writer.add_page(page)
                    writer.write(output_file)

                progress_callback(100.0 * (float(idx) / pages_len))

    def extract(self,
                output_file: Path,
                input_file: Path,
                pages: Sequence[int],
                password: str = "",
                progress_callback: Callable[[float], Any] = lambda p: p,
                ):
        """
        Extract specific pages from input files into a PDF output file.

        :param output_file: Output PDF file
        :param input_file: Input PDF file
        :param pages: List of pages to extract (0-indexed).
        :param password: Password used to decrypt file, if needed. Defaults to "" (do not decrypt).
        :param progress_callback: Progress callback (0-100). Defaults to a no-op.

        :raises FileNotFoundError: if input file not found
        """

        with PdfReader(input_file) as reader, PdfWriter() as writer:
            if password and reader.is_encrypted:
                reader.decrypt(password)

            pdf_len = len(reader.pages)
            pages_len = len(pages)
            for idx, page_num in enumerate(pages, start=1):
                if pdf_len <= page_num:
                    raise ValueError(f"PDF '{input_file}' has only {len(reader.pages)} pages. Cannot extract page {page_num + 1}.")
                writer.add_page(reader.pages[page_num])

                progress_callback(100.0 * (float(idx) / pages_len))
            writer.write(output_file)
            progress_callback(100.0)

    def rotate(self,
               output_file: Path,
               input_file: Path,
               rotations: dict[int, Rotation],
               decrypt_password: str = "",
               progress_callback: Callable[[float], Any] = lambda p: p,
               ):
        """
        Rotate specific pages from input files, generating a PDF output file.

        :param output_file: Output PDF file.
        :param input_file: Input PDF file.
        :param rotations: Dict format { page_num: rotation_degrees }. Rotation degrees must be one of the values in the Rotations enum.
        :param decrypt_password: Password used to decrypt file, if needed. Defaults to None (do not decrypt).
        :param progress_callback: Progress callback (0-100). Defaults to None.

        :raises FileNotFoundError: if input file not found        
        """
        with PdfReader(input_file) as reader, PdfWriter() as writer:
            if decrypt_password and reader.is_encrypted:
                reader.decrypt(decrypt_password)

            pages_len = len(reader.pages)
            for i, page in enumerate(reader.pages):
                rotation = rotations.get(i, self.Rotation.DEG_0)

                # execute page rotation
                logger.debug(f"Rotating page {i} by {rotation} deg")
                if rotation.value > 0:
                    page.rotate(rotation.value)  # clockwise: 90, 180, 270
                writer.add_page(page)

                progress_callback(100.0 * (float(i) / pages_len))

            # save output file
            writer.write(output_file)
            progress_callback(100.0)

    def encrypt(self,
                output_file: Path,
                input_file: Path,
                owner_password: str,
                user_password: str = "",
                decrypt_password: str = "",
                encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.AES_256,
                permissions: Iterable[EncryptionPermission] | None = None,
                progress_callback: Callable[[float], Any] = lambda p: p,
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
        with PdfReader(input_file) as reader, PdfWriter() as writer:
            if decrypt_password and reader.is_encrypted:
                reader.decrypt(decrypt_password)

            # set user permissions
            permissions_flag = PyPDFBackend.EncryptionPermission.NONE.get()
            for perm in permissions or []:
                permissions_flag |= perm.get()

            # add pages into writer
            pages_len = len(reader.pages)
            for i, page in enumerate(reader.pages, start=0):
                writer.add_page(page)
                progress_callback(100.0 * (float(i) / pages_len))

            # Encrypt with user and owner passwords
            writer.encrypt(
                owner_password=owner_password,
                user_password=user_password or owner_password,
                permissions_flag=permissions_flag,
                algorithm=encryption_algorithm.get(),
                use_128bit=True,
            )

            # save output file
            writer.write(output_file)
            progress_callback(100.0)

    def decrypt(self,
                output_file: Path,
                input_file: Path,
                password: str,
                progress_callback: Callable[[float], Any] = lambda p: p,
                ):
        """
        Decrypt input file, generating a non-protected PDF output file.

        :param output_file: Output PDF file.
        :param input_file: Input PDF file.
        :param password: Password used to decrypt file.
        :param progress_callback: Progress callback (0-100). Defaults to None.

        :raises FileNotFoundError: if input file not found
        """
        with PdfReader(input_file) as reader, PdfWriter() as writer:
            # decrypt file
            if reader.is_encrypted:
                reader.decrypt(password)

            # Generate decrypted pdf
            pages_len = len(reader.pages)
            for i, page in enumerate(reader.pages, start=0):
                writer.add_page(page)
                progress_callback(100.0 * (float(i) / pages_len))

            # save file
            writer.write(output_file)
            progress_callback(100.0)


__all__ = [
    "PyPDFBackend",
]
