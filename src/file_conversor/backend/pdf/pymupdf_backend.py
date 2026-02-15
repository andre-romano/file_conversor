# src\file_conversor\backend\pymupdf_backend.py

"""
This module provides functionalities for handling files using ``pymupdf`` backend.
"""

from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterable, cast

from file_conversor.backend.abstract_backend import AbstractBackend

# user-provided imports
from file_conversor.config import Log, get_translation


LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()


class PyMuPDFBackend(AbstractBackend):
    """
    A class that provides an interface for handling files using ``pymupdf``.
    """

    class SupportedInFormats(Enum):
        PDF = "pdf"

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
                password: str = "",
                ):
        """
        Convert input files into output file.

        :param output_file: Output file
        :param input_file: Input file. 
        :param dpi: DPI for rendering images. Defaults to 200.
        :param password: Password for encrypted PDF files. Defaults to "" (do not decrypt).

        :raises FileNotFoundError: if input file not found
        :raises ValueError: if output format is unsupported
        """
        import fitz  # pyright: ignore[reportMissingTypeStubs] # pymupdf
        # open file
        with fitz.open(str(input_file)) as doc:
            if doc.is_encrypted:
                if not password:
                    raise ValueError(_("Password is required for encrypted PDF files"))
                doc.authenticate(password)  # pyright: ignore[reportUnknownMemberType]
            # => .png, .jpg, .svg OUTPUT
            for page in doc:  # pyright: ignore[reportUnknownVariableType]
                pix = page.get_pixmap(dpi=dpi)  # type: ignore
                pix.save(f"{output_file.with_suffix("")}_{page.number + 1}{output_file.suffix}")  # type: ignore

    def extract_images(
            self,
            input_file: Path,
            output_dir: Path,
            overwrite_output: bool,
            progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        """
        Extract all images from a PDF using PyMuPDF (fitz).
        Saves images in their native formats.
        """
        import fitz  # pyright: ignore[reportMissingTypeStubs] # pymupdf

        with fitz.open(input_file) as doc:
            page_len = len(doc)
            for page_index, page in enumerate(doc, start=1):  # type: ignore
                images = cast(Iterable[Any],
                              page.get_images(full=True))  # pyright: ignore[reportUnknownMemberType]

                for img_index, img in enumerate(images, start=1):
                    xref = img[0]  # xref number of the image
                    base_image = cast(dict[str, Any],
                                      doc.extract_image(xref))  # pyright: ignore[reportUnknownMemberType]

                    img_bytes: bytes = base_image["image"]
                    ext: str = base_image["ext"]  # format: png, jpg, jp2, etc.

                    output_file = output_dir / f"{input_file.stem}_page{page_index}_img{img_index}.{ext}"
                    if not overwrite_output and output_file.exists():
                        raise FileExistsError(f"{_('File')} '{output_file}' {_('exists')}")

                    with open(output_file, "wb") as f:
                        f.write(img_bytes)

                    # logger.debug(f"Extracted {output_file} ({width}x{height})")

                progress = 100.0 * (float(page_index) / page_len)
                progress_callback(progress)
        progress_callback(100.0)


__all__ = [
    "PyMuPDFBackend",
]
