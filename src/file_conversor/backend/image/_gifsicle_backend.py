# src\file_conversor\backend\gifsicle_backend.py

"""
This module provides functionalities for handling files using gifsicle.
"""

from pathlib import Path
from rich import print

# user-provided imports
from file_conversor.config import Environment, Log
from file_conversor.config.locale import get_translation

from file_conversor.dependency import BrewPackageManager, ScoopPackageManager
from file_conversor.backend.abstract_backend import AbstractBackend

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class _GifSicleBackend(AbstractBackend):  # pyright: ignore[reportUnusedClass]
    """
    Provides an interface for handling files using gifsicle.
    """

    SUPPORTED_IN_FORMATS = {
        'gif': {},
    }
    SUPPORTED_OUT_FORMATS = {
        'gif': {},
    }
    EXTERNAL_DEPENDENCIES: set[str] = {
        "gifsicle",
    }

    def __init__(
        self,
        install_deps: bool | None,
        verbose: bool = False,
    ):
        """
        Initialize the backend.

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action. 
        :param verbose: Verbose logging. Defaults to False.      

        :raises RuntimeError: if dependency is not found
        """
        super().__init__(
            pkg_managers={
                ScoopPackageManager({
                    "gifsicle": "gifsicle"
                }),
                BrewPackageManager({
                    "gifsicle": "gifsicle"
                }),
            },
            install_answer=install_deps,
        )
        self._verbose = verbose

        # check binary
        self._bin = self.find_in_path("gifsicle")

    def compress(
        self,
            input_file: str | Path,
            output_file: str | Path,
            compression_level: int = 3,
            **kwargs,
    ):
        """
        Execute command to compress the input file.

        :param input_file: Input file path.
        :param output_file: Output file path.              
        :param compression_level: Image compression level (0-3). Defaults to 3 (max compression).              
        :param kwargs: Optional arguments.

        :return: Subprocess.CompletedProcess object
        """

        # Execute the command
        process = Environment.run(
            f"{self._bin}",
            f"-O={compression_level}",
            f"{input_file}",
            f"-o", f"{output_file}",
        )
        return process


__all__ = [
    "_GifSicleBackend",
]
