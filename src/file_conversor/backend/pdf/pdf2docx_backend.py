# src\file_conversor\backend\pdf2docx_backend.py

"""
This module provides functionalities for handling files using ``pdf2docx`` backend.
"""
import pdf2docx
from pathlib import Path

from typing import Any, Callable

# user-provided imports
from file_conversor.config import Environment, Log, State
from file_conversor.config.locale import get_translation

from file_conversor.backend.abstract_backend import AbstractBackend

STATE = State.get_instance()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()


class PDF2DOCXBackend(AbstractBackend):
    """
    A class that provides an interface for handling files using ``pdf2docx``.
    """

    SUPPORTED_IN_FORMATS = {
        "pdf": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "docx": {},
    }
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
                password: str | None = None,
                ):
        """
        Convert input files into output file.

        :param output_file: Output file
        :param input_file: Input file. 
        :param password: Password for encrypted PDF files. Defaults to "".

        :raises FileNotFoundError: if input file not found
        :raises ValueError: if output format is unsupported
        """

        input_file = Path(input_file).resolve()
        output_file = Path(output_file).resolve()

        self.check_file_exists(input_file)

        converter = pdf2docx.Converter(
            str(input_file),
            password=password,  # pyright: ignore[reportArgumentType]
        )
        if converter.fitz_doc.is_encrypted and not password:
            raise ValueError(_("Password is required for encrypted PDF files"))
        converter.convert(
            str(output_file),
        )


__all__ = [
    "PDF2DOCXBackend",
]
