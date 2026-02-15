# src\file_conversor\backend\pikepdf_backend.py

"""
This module provides functionalities for handling PDF files using ``pikepdf`` backend (qpdf python wrapper).
"""

from enum import Enum
from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.abstract_backend import AbstractBackend

# user-provided imports
from file_conversor.config.log import Log


LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class PikePDFBackend(AbstractBackend):
    """
    A class that provides an interface for handling PDF files using ``pikepdf`` (qpdf python wrapper).
    """

    class SupportedInFormats(Enum):
        PDF = "pdf"

    class SupportedOutFormats(Enum):
        PDF = "pdf"

    EXTERNAL_DEPENDENCIES: set[str] = set()

    def __init__(
        self,
        verbose: bool = False,
    ):
        """
        Initialize the ``pikepdf`` backend

        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__()
        self._verbose = verbose

    @staticmethod
    def is_encrypted(file_path: str | Path) -> bool:
        """Checks if PDF file is encrypted"""
        import pikepdf
        try:
            with pikepdf.open(file_path):
                return False  # opened without password → not encrypted
        except pikepdf.PasswordError:
            return True  # opening failed because it's encrypted

    def compress(
        self,
        input_file: Path,
        output_file: Path,
        linearize: bool = True,
        decrypt_password: str = "",
        progress_callback: Callable[[int], Any] | None = None,
    ):
        """
        Compress input PDF file.

        :param input_files: Input PDF file. 
        :param output_files: Output PDF file.
        :param linearize: Linearize PDF file structures (speed up web render). Defaults to True.
        :param decryption_password: Decryption password for input PDF file. Defaults to "" (do not decrypt).
        :param progress_callback: Progress callback executed as PDF is processed. Format callback(0-100). Defaults to None (no progress callback).

        :raises FileNotFoundError: if input file not found.
        :raises PDFError, ForeignObjectError: if qpdf errors.
        """
        import pikepdf

        from pikepdf import ObjectStreamMode

        # Open PDF (with password if provided)
        preserve_encryption: bool = (decrypt_password != "" and self.is_encrypted(input_file))
        with pikepdf.open(input_file, password=decrypt_password) as pdf:
            # Save optimized PDF
            pdf.save(output_file,
                     encryption=preserve_encryption,  # preserve encryption
                     linearize=linearize,  # linearize for web
                     compress_streams=True,  # compress streams
                     object_stream_mode=ObjectStreamMode(ObjectStreamMode.generate),  # generate streams as needed (max compression)
                     progress=progress_callback,  # callback(0-100)
                     )


__all__ = [
    "PikePDFBackend",
]
