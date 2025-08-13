# src\file_conversor\backend\pikepdf_backend.py

"""
This module provides functionalities for handling PDF files using ``pikepdf`` backend (qpdf python wrapper).
"""

import pikepdf

from pikepdf import ObjectStreamMode
from typing import Any, Callable

# user-provided imports
from file_conversor.config.log import Log

from file_conversor.backend.abstract_backend import AbstractBackend

LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class PikePDFBackend(AbstractBackend):
    """
    A class that provides an interface for handling PDF files using ``pikepdf`` (qpdf python wrapper).
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
        Initialize the ``pikepdf`` backend

        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__()
        self._verbose = verbose

    @staticmethod
    def is_encrypted(file_path: str) -> bool:
        """Checks if PDF file is encrypted"""
        try:
            with pikepdf.open(file_path):
                return False  # opened without password → not encrypted
        except pikepdf.PasswordError:
            return True  # opening failed because it's encrypted
        except Exception as e:
            raise e  # other errors (corrupted file, etc.)

    def repair(
        self,
        input_file: str,
        output_file: str,
        progress_callback: Callable[[int], Any] | None = None,
        decrypt_password: str | None = None,
        compress: bool = True,
    ):
        """
        Repair input PDF file.

        :param input_files: Input PDF file. 
        :param output_files: Output PDF file.
        :param progress_callback: Progress callback executed as PDF is processed. Format callback(0-100). Defaults to None (no progress callback).
        :param decryption_password: Decryption password for input PDF file. Defaults to None (do not decrypt).
        :param compress: Compress PDF output file structures. Defaults to True (compress structures, losslessly).

        :raises FileNotFoundError: if input file not found.
        :raises PDFError, ForeignObjectError: if qpdf errors.
        """
        self.check_file_exists(input_file)

        # Open PDF (with password if provided)
        preserve_encryption = True if decrypt_password and self.is_encrypted(input_file) else None
        with pikepdf.open(input_file, password=decrypt_password if decrypt_password else "") as pdf:
            # Save optimized PDF
            pdf.save(output_file,
                     progress=progress_callback,  # callback(0-100)
                     encryption=preserve_encryption,  # preserve encryption
                     compress_streams=compress,  # compress streams
                     object_stream_mode=ObjectStreamMode(ObjectStreamMode.generate),  # generate streams as needed (max compression)
                     )
