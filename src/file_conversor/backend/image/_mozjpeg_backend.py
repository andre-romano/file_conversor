# src\file_conversor\backend\mozjpeg_backend.py

"""
This module provides functionalities for handling files using mozjpeg.
"""
from enum import Enum
from pathlib import Path
from typing import Any

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.config import Environment, Log
from file_conversor.config.locale import get_translation
from file_conversor.dependency import BrewPackageManager, ScoopPackageManager


_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class MozJPEGBackend(AbstractBackend):  # pyright: ignore[reportUnusedClass]
    """
    Provides an interface for handling files using mozjpeg.
    """

    class SupportedInFormats(Enum):
        JPG = "jpg"
        JPEG = "jpeg"

    class SupportedOutFormats(Enum):
        JPG = "jpg"

    EXTERNAL_DEPENDENCIES: set[str] = {
        "cjpeg",
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
                    "cjpeg": "mozjpeg"
                }),
                BrewPackageManager({
                    "cjpeg": "mozjpeg"
                }),
            },
            install_answer=install_deps,
        )
        self._verbose = verbose

        # check ffprobe / ffmpeg
        self._mozjpeg_bin = self.find_in_path("cjpeg")

    def compress(
        self,
        input_file: str | Path,
        output_file: str | Path,
        quality: int,
        **kwargs: Any,  # noqa: ARG002
    ):
        """
        Execute the command to compress the input file.

        :param input_file: Input file path.
        :param output_file: Output file path.      
        :param quality: Output image quality.              
        :param kwargs: Optional arguments.

        :return: Subprocess.CompletedProcess object

        :raises RuntimeError: If backend encounters an error during execution.
        """
        import subprocess

        # Execute the command
        process = Environment.run(
            f"{self._mozjpeg_bin}",
            f"-quality", f"{quality}",
            f"-progressive",
            f"-optimize",
            f"{input_file}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
        )

        # Save the compressed output to file
        with open(output_file, "wb") as fp:
            fp.write(process.stdout)
        return process


__all__ = [
    "MozJPEGBackend",
]
