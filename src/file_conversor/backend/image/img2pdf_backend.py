# src\file_conversor\backend\img2pdf_backend.py

"""
This module provides functionalities for handling PDF files using ``img2pdf`` backend.
"""

import img2pdf

from pathlib import Path
from datetime import datetime
from typing import Any, Iterable

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend


class Img2PDFBackend(AbstractBackend):
    """
    A class that provides an interface for handling PDF files using ``img2pdf``.
    """

    FIT_MODES = {
        'into': img2pdf.FitMode.into,
        'fill': img2pdf.FitMode.fill,
    }

    PAGE_LAYOUT = {
        'a4': (21.00, 29.70),  # A4 in cm
        'a4_landscape': (29.70, 21.00),
    }

    SUPPORTED_IN_FORMATS = {
        "jpeg": {},
        "jpg": {},
        "png": {},
        "tiff": {},
        "tif": {},
        "bmp": {},
        "gif": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "pdf": {},
    }
    EXTERNAL_DEPENDENCIES: set[str] = set()

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

    def to_pdf(self,
               output_file: str | Path,
               input_files: Iterable[str | Path],
               image_fit: img2pdf.FitMode = FIT_MODES['into'],
               page_size: tuple[float, float] | None = None,
               dpi: int = 200,
               include_metadata: bool = True
               ):
        """
        Convert input image files into one PDF output file.

        image_fit = 
        - FIT_INTO: resize image to fit in page (keep proportions, DO NOT cut image)
        - FIT_FILL: resize image to page - no borders allowed (keep proportions, CUT image if necessary)

        dpi = 
        -  96 = low quality, for screen.
        - 200 = good quality, for screen.
        - 300 = high quality, for printing.

        :param output_file: Output PDF file
        :param input_files: Input image files. 
        :param image_fit: Where and how to place fig. Valid only when ``page_size`` != None. Defaults to FIT_INTO.
        :param page_size: PDF page size, in centimeters (cm). Format (width, height). Defaults to LAYOUT_NONE (PDF size is exactly the size of figs).
        :param dpi: Set dots per inch (DPI) for picture. Defaults to 200.
        :param include_metadata: Include basic metadata (moddata, createdate, creator, etc). Defaults to True.

        :raises FileNotFoundError: if input file not found
        """
        for input_file in input_files:
            self.check_file_exists(input_file)
        output_path = Path(output_file).with_suffix(".pdf")

        # get current day
        now = datetime.now()
        opts: dict[str, Any] = {
            'dpi': dpi,
        }

        # metadata
        if include_metadata:
            opts.update({
                # PDF metadata
                'creationdate': now,
                'moddate': now,
                'creator': "img2pdf",
                'producer': "img2pdf",
            })

        # page layout
        if page_size:
            opts['layout_fun'] = img2pdf.get_layout_fun(
                pagesize=tuple(img2pdf.cm_to_pt(x) for x in page_size),
                fit=image_fit,
            )

        buffer = img2pdf.convert(*input_files, **opts)
        if not buffer:
            raise RuntimeError(f"Error converting files to PDF: {input_files}")

        with open(output_path, "wb") as f:
            f.write(buffer)


__all__ = [
    "Img2PDFBackend",
]
