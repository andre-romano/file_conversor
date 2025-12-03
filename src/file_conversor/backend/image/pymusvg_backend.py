# src\file_conversor\backend\pymusvg_backend.py

"""
This module provides functionalities for handling SVG files using ``pymupdf`` backend.
"""

import fitz  # pymupdf

from pathlib import Path

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend


class PyMuSVGBackend(AbstractBackend):
    """
    A class that provides an interface for handling SVG files using ``pymupdf``.
    """

    SUPPORTED_IN_FORMATS = {
        "svg": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "png": {},
        "jpg": {},
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
                dpi: int = 200,
                ):
        """
        Convert input image files into output file.

        :param output_file: Output file
        :param input_file: Input file. 
        :param dpi: DPI for rendering images. Defaults to 200.

        :raises FileNotFoundError: if input file not found
        :raises ValueError: if output format is unsupported
        """
        input_file = Path(input_file).resolve()
        output_file = Path(output_file).resolve()

        self.check_file_exists(input_file)

        # open file
        doc = fitz.open(str(input_file))

        # => .png, .jpg OUTPUT
        for page in doc:
            pix = page.get_pixmap(dpi=dpi)  # type: ignore
            pix.save(str(output_file))  # type: ignore


__all__ = [
    "PyMuSVGBackend",
]
