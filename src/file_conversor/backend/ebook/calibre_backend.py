# src\file_conversor\backend\ebook\calibre_backend.py

"""
This module provides functionalities for handling ebook files using Calibre.
"""

from enum import Enum
from pathlib import Path

from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.config import Environment, Log, get_translation
from file_conversor.dependency import BrewPackageManager, ScoopPackageManager


_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class CalibreBackend(AbstractBackend):
    """
    CalibreBackend is a class that provides an interface for handling ebook files using Calibre.
    """

    class SupportedInFormats(Enum):
        AZW = "azw"
        AZW3 = "azw3"
        AZW4 = "azw4"
        CBR = "cbr"
        CBZ = "cbz"
        EPUB = "epub"
        FB2 = "fb2"
        MOBI = "mobi"

    class SupportedOutFormats(Enum):
        AZW3 = "azw3"
        DOCX = "docx"
        EPUB = "epub"
        FB2 = "fb2"
        MOBI = "mobi"
        PDF = "pdf"

    EXTERNAL_DEPENDENCIES: set[str] = {
        "ebook-convert",
    }

    def __init__(
        self,
        install_deps: bool | None,
        verbose: bool = False,
    ):
        """
        Initialize the Calibre backend.

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action. 
        :param verbose: Verbose logging. Defaults to False.      

        :raises RuntimeError: if calibre dependency is not found
        """
        super().__init__(
            pkg_managers={
                ScoopPackageManager({
                    "ebook-convert": "calibre"
                }, buckets=[
                    "extras",
                ], env=[
                    rf"{Path.home()}\scoop\shims"
                ]),
                BrewPackageManager({
                    "ebook-convert": "calibre"
                }),
            },
            install_answer=install_deps,
        )
        self._install_deps = install_deps
        self._verbose = verbose

        # check ebook-convert
        self._ebook_convert_bin = self.find_in_path("ebook-convert")

    def convert(
        self,
        output_file: str | Path,
        input_file: str | Path,
    ):
        """
        Convert input file into an output file.

        :param output_file: Output file.
        :param input_file: Input file.        

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        input_path = Path(input_file).resolve()
        output_path = Path(output_file).resolve()

        # Execute command
        process = Environment.run(
            str(self._ebook_convert_bin),
            str(input_path),
            str(output_path),
        )
        return process


__all__ = [
    'CalibreBackend',
]
