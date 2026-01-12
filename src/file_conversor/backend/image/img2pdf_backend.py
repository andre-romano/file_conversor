# src\file_conversor\backend\img2pdf_backend.py

"""
This module provides functionalities for handling PDF files using ``img2pdf`` backend.
"""

import img2pdf

from pathlib import Path
from datetime import datetime

from typing import Any, Iterable
from enum import Enum

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend


class Img2PDFBackend(AbstractBackend):
    """
    A class that provides an interface for handling PDF files using ``img2pdf``.
    """

    class FitMode(Enum):
        INTO = "into"
        FILL = "fill"

        def get(self) -> img2pdf.FitMode:
            if self == Img2PDFBackend.FitMode.INTO:
                return img2pdf.FitMode.into
            elif self == Img2PDFBackend.FitMode.FILL:
                return img2pdf.FitMode.fill
            else:
                raise ValueError(f"Invalid FitMode: {self}")

    class PageLayout(Enum):
        A0 = "a0"
        A0_LANDSCAPE = "a0-landscape"

        A1 = "a1"
        A1_LANDSCAPE = "a1-landscape"

        A2 = "a2"
        A2_LANDSCAPE = "a2-landscape"

        A3 = "a3"
        A3_LANDSCAPE = "a3-landscape"

        A4 = "a4"
        A4_LANDSCAPE = "a4-landscape"

        LETTER = "letter"
        LETTER_LANDSCAPE = "letter-landscape"

        def get(self) -> tuple[float, float]:
            if self == Img2PDFBackend.PageLayout.A0:
                return (84.10, 118.90)  # A0 in cm
            elif self == Img2PDFBackend.PageLayout.A0_LANDSCAPE:
                return (118.90, 84.10)  # A0 Landscape in cm
            elif self == Img2PDFBackend.PageLayout.A1:
                return (59.40, 84.10)  # A1 in cm
            elif self == Img2PDFBackend.PageLayout.A1_LANDSCAPE:
                return (84.10, 59.40)  # A1 Landscape in cm
            elif self == Img2PDFBackend.PageLayout.A2:
                return (42.00, 59.40)  # A2 in cm
            elif self == Img2PDFBackend.PageLayout.A2_LANDSCAPE:
                return (59.40, 42.00)  # A2 Landscape in cm
            elif self == Img2PDFBackend.PageLayout.A3:
                return (29.70, 42.00)  # A3 in cm
            elif self == Img2PDFBackend.PageLayout.A3_LANDSCAPE:
                return (42.00, 29.70)  # A3 Landscape in cm
            elif self == Img2PDFBackend.PageLayout.A4:
                return (21.00, 29.70)  # A4 in cm
            elif self == Img2PDFBackend.PageLayout.A4_LANDSCAPE:
                return (29.70, 21.00)  # A4 Landscape in cm
            elif self == Img2PDFBackend.PageLayout.LETTER:
                return (21.59, 27.94)  # Letter in cm
            elif self == Img2PDFBackend.PageLayout.LETTER_LANDSCAPE:
                return (27.94, 21.59)  # Letter Landscape in cm
            else:
                raise ValueError(f"Invalid PageLayout: {self}")

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
               image_fit: FitMode = FitMode.INTO,
               page_size: tuple[float, float] | PageLayout | None = None,
               dpi: int = 200,
               include_metadata: bool = True
               ):
        """
        Convert input image files into one PDF output file.

        image_fit = 
        - into: resize image to fit in page (keep proportions, DO NOT cut image)
        - fill: resize image to page - no borders allowed (keep proportions, CUT image if necessary)

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
            page_sz: tuple[float, float]
            if isinstance(page_size, tuple):
                page_sz = page_size
            else:
                page_sz = page_size.get()
            opts['layout_fun'] = img2pdf.get_layout_fun(
                pagesize=tuple(img2pdf.cm_to_pt(x) for x in page_sz),
                fit=image_fit.get(),
            )

        buffer = img2pdf.convert(*input_files, **opts)
        if not buffer:
            raise RuntimeError(f"Error converting files to PDF: {input_files}")

        with open(output_path, "wb") as f:
            f.write(buffer)


__all__ = [
    "Img2PDFBackend",
]
