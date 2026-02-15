# src\file_conversor\backend\pdf2docx_backend.py

"""
This module provides functionalities for handling files using ``pdf2docx`` backend.
"""

from enum import Enum
from pathlib import Path

from file_conversor.backend.abstract_backend import AbstractBackend

# user-provided imports
from file_conversor.config import Log, get_translation


LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()


class PDF2DOCXBackend(AbstractBackend):
    """
    A class that provides an interface for handling files using ``pdf2docx``.
    """

    class SupportedInFormats(Enum):
        PDF = "pdf"

    class SupportedOutFormats(Enum):
        DOCX = "docx"

    EXTERNAL_DEPENDENCIES: set[str] = set()

    def __init__(
        self,
        verbose: bool = False,
    ):
        """
        Initialize the backend

        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__()
        self._verbose = verbose

    def convert(self,
                output_file: str | Path,
                input_file: str | Path,
                password: str = "",
                ):
        """
        Convert input files into output file.

        :param output_file: Output file
        :param input_file: Input file. 
        :param password: Password for encrypted PDF files. Defaults to "".

        :raises FileNotFoundError: if input file not found
        :raises ValueError: if output format is unsupported
        """
        import pdf2docx  # pyright: ignore[reportMissingTypeStubs]

        input_file = Path(input_file).resolve()
        output_file = Path(output_file).resolve()

        self.check_file_exists(input_file)

        converter = pdf2docx.Converter(
            str(input_file),
            password=password or None,  # pyright: ignore[reportArgumentType]
        )
        if converter.fitz_doc.is_encrypted and not password:
            raise ValueError(_("Password is required for encrypted PDF files"))
        converter.convert(  # pyright: ignore[reportUnknownMemberType]
            str(output_file),
        )
        converter.close()


__all__ = [
    "PDF2DOCXBackend",
]
