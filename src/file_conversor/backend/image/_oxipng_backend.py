# src\file_conversor\backend\oxipng_backend.py

"""
This module provides functionalities for handling files using oxipng.
"""

import shutil

from pathlib import Path
from rich import print

# user-provided imports
from file_conversor.config import Environment, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.validators import check_file_format

from file_conversor.dependency import BrewPackageManager, ScoopPackageManager
from file_conversor.backend.abstract_backend import AbstractBackend

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class _OxiPNGBackend(AbstractBackend):  # pyright: ignore[reportUnusedClass]
    """
    Provides an interface for handling files using oxipng.
    """

    SUPPORTED_IN_FORMATS = {
        'png': {},
    }
    SUPPORTED_OUT_FORMATS = {
        'png': {},
    }
    EXTERNAL_DEPENDENCIES: set[str] = {
        "oxipng",
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
                    "oxipng": "oxipng"
                }),
                BrewPackageManager({
                    "oxipng": "oxipng"
                }),
            },
            install_answer=install_deps,
        )
        self._verbose = verbose

        # check binary
        self._oxipng_bin = self.find_in_path("oxipng")

    def compress(
        self,
            input_file: str | Path,
            output_file: str | Path,
            strip_metadata: bool = True,
            compression_level: int = 6,
            **kwargs,
    ):
        """
        Execute command to compress the input file.

        :param input_file: Input file path.
        :param output_file: Output file path.      
        :param strip_metadata: True to remove metadata from image, False to preserve metadata. Defaults to True.
        :param compression_level: Image compression level (0-6). Defaults to 6 (max compression).              
        :param kwargs: Optional arguments.

        :return: Subprocess.CompletedProcess object
        """
        # copy input to output
        shutil.copy2(src=input_file, dst=output_file)

        # build command
        command = [
            f"{self._oxipng_bin}",
            f"-o", f"{compression_level}",
        ]
        if strip_metadata:
            command.extend([f"--strip", f"safe",])
        command.append(f"{output_file}")

        # Execute the command
        process = Environment.run(
            *command,
        )
        return process


__all__ = [
    "_OxiPNGBackend",
]
