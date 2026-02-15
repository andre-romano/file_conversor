# src\file_conversor\backend\pymusvg_backend.py

"""
This module provides functionalities for handling SVG files using ``pymupdf`` backend.
"""

from enum import Enum
from pathlib import Path

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend


class PyMuSVGBackend(AbstractBackend):
    """
    A class that provides an interface for handling SVG files using ``pymupdf``.
    """

    class SupportedInFormats(Enum):
        SVG = "svg"

    class SupportedOutFormats(Enum):
        PNG = "png"
        JPG = "jpg"

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
                output_file: Path,
                input_file: Path,
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
        import fitz  # pyright: ignore[reportMissingTypeStubs] # pymupdf

        # open file
        doc = fitz.open(str(input_file))

        for page in doc:  # pyright: ignore[reportUnknownVariableType]
            pix = page.get_pixmap(dpi=dpi)   # pyright: ignore[reportUnknownVariableType, reportAttributeAccessIssue, reportUnknownMemberType]
            pix.save(str(output_file))   # pyright: ignore[reportUnknownMemberType]


__all__ = [
    "PyMuSVGBackend",
]
