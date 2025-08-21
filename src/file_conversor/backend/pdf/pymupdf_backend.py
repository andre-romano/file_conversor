# src\file_conversor\backend\pymupdf_backend.py

"""
This module provides functionalities for handling files using ``pymupdf`` backend.
"""

import fitz  # pymupdf

from pathlib import Path

from typing import Any, Callable

# user-provided imports
from file_conversor.config import Environment, Log

from file_conversor.backend.abstract_backend import AbstractBackend

LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class PyMuPDFBackend(AbstractBackend):
    """
    A class that provides an interface for handling files using ``pymupdf``.
    """

    SUPPORTED_IN_FORMATS = {
        "pdf": {},
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
        Convert input files into output file.

        :param output_file: Output file
        :param input_file: Input file. 
        :param dpi: DPI for rendering images. Defaults to 200.

        :raises FileNotFoundError: if input file not found
        :raises ValueError: if output format is unsupported
        """
        self.check_file_exists(input_file)
        in_path = Path(input_file)
        out_path = Path(output_file)

        # open file
        with fitz.open(input_file) as doc:
            # => .png, .jpg, .svg OUTPUT
            for page in doc:
                pix = page.get_pixmap(dpi=dpi)  # type: ignore
                pix.save(f"{out_path.with_suffix("")}_{page.number + 1}{out_path.suffix}")  # type: ignore

    def extract_images(
            self,
            input_path: str | Path,
            output_dir: str | Path,
            progress_callback: Callable[[float], Any] | None = None,
    ):
        """
        Extract all images from a PDF using PyMuPDF (fitz).
        Saves images in their native formats.
        """
        input_path = Path(input_path)
        input_name = input_path.with_suffix("").name

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        with fitz.open(input_path) as doc:
            page_len = len(doc)
            for page_index, page in enumerate(doc, start=1):  # type: ignore
                images = page.get_images(full=True)  # list of image xrefs
                img_len = len(images)

                # if img_len > 0:
                #     logger.debug(f"Page {page_index}: {img_len} image(s) found")

                for img_index, img in enumerate(images, start=1):
                    xref = img[0]  # xref number of the image
                    base_image = doc.extract_image(xref)

                    img_bytes = base_image["image"]
                    ext = base_image["ext"]  # format: png, jpg, jp2, etc.
                    width, height = base_image["width"], base_image["height"]

                    fname = output_dir / f"{input_name}_page{page_index}_img{img_index}.{ext}"
                    with open(fname, "wb") as f:
                        f.write(img_bytes)

                    # logger.debug(f"Extracted {fname} ({width}x{height})")

                progress = 100.0 * (float(page_index) / page_len)
                if progress_callback:
                    progress_callback(progress)
