# src\file_conversor\backend\pymupdf_backend.py

"""
This module provides functionalities for handling files using ``pymupdf`` backend.
"""

import fitz  # pymupdf

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
                password: str | None = None,
                ):
        """
        Convert input files into output file.

        :param output_file: Output file
        :param input_file: Input file. 
        :param dpi: DPI for rendering images. Defaults to 200.
        :param password: Password for encrypted PDF files. Defaults to None.

        :raises FileNotFoundError: if input file not found
        :raises ValueError: if output format is unsupported
        """
        input_file = Path(input_file).resolve()
        output_file = Path(output_file).resolve()

        self.check_file_exists(input_file)

        # open file
        with fitz.open(str(input_file)) as doc:
            if doc.is_encrypted:
                if not password:
                    raise ValueError(_("Password is required for encrypted PDF files"))
                doc.authenticate(password or "")
            # => .png, .jpg, .svg OUTPUT
            for page in doc:
                pix = page.get_pixmap(dpi=dpi)  # type: ignore
                pix.save(f"{output_file.with_suffix("")}_{page.number + 1}{output_file.suffix}")  # type: ignore

    def extract_images(
            self,
            input_file: str | Path,
            output_dir: str | Path,
            progress_callback: Callable[[float], Any] | None = None,
    ):
        """
        Extract all images from a PDF using PyMuPDF (fitz).
        Saves images in their native formats.
        """
        input_file = Path(input_file)
        input_name = input_file.with_suffix("").name

        output_dir = Path(output_dir)

        with fitz.open(input_file) as doc:
            page_len = len(doc)
            for page_index, page in enumerate(doc, start=1):  # type: ignore
                images = page.get_images(full=True)  # list of image xrefs

                for img_index, img in enumerate(images, start=1):
                    xref = img[0]  # xref number of the image
                    base_image = doc.extract_image(xref)

                    img_bytes = base_image["image"]
                    ext = base_image["ext"]  # format: png, jpg, jp2, etc.

                    output_file = output_dir / f"{input_name}_page{page_index}_img{img_index}.{ext}"
                    if not STATE["overwrite-output"] and Path(output_file).exists():
                        raise FileExistsError(f"{_('File')} '{output_file}' {_('exists')}")

                    with open(output_file, "wb") as f:
                        f.write(img_bytes)

                    # logger.debug(f"Extracted {output_file} ({width}x{height})")

                progress = 100.0 * (float(page_index) / page_len)
                if progress_callback:
                    progress_callback(progress)
        if progress_callback:
            progress_callback(100.0)


__all__ = [
    "PyMuPDFBackend",
]
