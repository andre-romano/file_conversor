# src\file_conversor\backend\pdf2docx_backend.py

"""
This module provides functionalities for handling PDF files using ``pdf2docx`` backend.
"""
from pdf2docx import Converter

from typing import Iterable

# user-provided imports
from file_conversor.config import Log

from file_conversor.backend.abstract_backend import AbstractBackend

LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class Pdf2DocxBackend(AbstractBackend):
    """
    A class that provides an interface for handling PDF files using ``pdf2docx``.
    """

    SUPPORTED_IN_FORMATS = {
        "pdf": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "docx": {},
    }

    def __init__(
        self,
        verbose: bool = False,
    ):
        """
        Initialize the ``pdf2docx`` backend

        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__()
        self._verbose = verbose

    def to_docx(
        self,
        output_file: str,
        input_file: str,
    ):
        """
        Convert input PDF file into an output DOCX file.

        :param output_file: Output DOCX file.
        :param input_file: Input PDF file.        

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        print(input_file)
        print(output_file)
        cv = Converter(input_file)
        cv.convert(output_file)
        cv.close()
