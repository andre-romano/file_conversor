# src\file_conversor\backend\pymupdf_backend.py

"""
This module provides functionalities for handling files using ``pymupdf`` backend.
"""

import fitz  # pymupdf
from pathlib import Path

from datetime import datetime
from typing import Any, Iterable

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend


class PyMuPDFBackend(AbstractBackend):
    """
    A class that provides an interface for handling files using ``pymupdf``.
    """

    SUPPORTED_IN_FORMATS = {
        "svg": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "png": {},
        "jpg": {},
    }

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
                output_file: str,
                input_file: str,
                dpi: int = 200,
                ):
        """
        Convert input image files into output file.

        :param output_file: Output file
        :param input_file: Input file. 
        :param dpi: DPI for rendering SVG. Defaults to 200.

        :raises FileNotFoundError: if input file not found
        :raises ValueError: if output format is unsupported
        """
        self.check_file_exists(input_file)

        doc = fitz.open(input_file)
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=dpi)  # type: ignore
        pix.save(output_file)
