# src\file_conversor\backend\ghostscript_backend.py

"""
This module provides functionalities for handling files using ``ghostscript`` backend.
"""

import subprocess
from pathlib import Path

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation

from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.dependency import ScoopPackageManager, BrewPackageManager

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class GhostscriptBackend(AbstractBackend):
    """
    A class that provides an interface for handling files using ``ghostscript``.
    """

    SUPPORTED_IN_FORMATS = {
        "pdf": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "pdf": {},
    }

    COMPRESSION_HIGH = "screen"
    """72 dpi quality - high compression / low quality"""

    COMPRESSION_MEDIUM = "ebook"
    """150 dpi quality - medium compression / medium quality"""

    COMPRESSION_LOW = "printer"
    """300 dpi quality - low compression / high quality"""

    COMPRESSION_NONE = "preprint"
    """600 dpi quality - no compression / highest quality"""

    def __init__(
        self,
        install_deps: bool | None,
        verbose: bool = False,
    ):
        """
        Initialize the FFMpeg backend.

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action. 

        :raises RuntimeError: if ffmpeg dependency is not found
        """
        super().__init__(
            pkg_managers={
                ScoopPackageManager({
                    "gs": "ghostscript"
                }),
                BrewPackageManager({
                    "gs": "ghostscript"
                }),
            },
            install_answer=install_deps,
        )
        self._verbose = verbose

        # find ghostscript bin
        self._ghostscript_bin = self.find_in_path("gs")

    def compress(self,
                 output_file: str,
                 input_file: str,
                 compression_level: str,
                 compatibility_preset: str = "1.5",
                 ):
        """
        Compress input PDF files.

        :param output_file: Output file
        :param input_file: Input file.         
        :param compression_level: Compression level.
        :param compatibility_level: PDF compatibility level (1.3 - 1.7). Defaults to 1.5 (good compatibility / stream compression support).

        :raises FileNotFoundError: if input file not found
        :raises ValueError: if output format is unsupported
        """
        self.check_file_exists(input_file)
        in_path = Path(input_file)
        out_path = Path(output_file)

        if compression_level not in [
            self.COMPRESSION_HIGH,
            self.COMPRESSION_MEDIUM,
            self.COMPRESSION_LOW,
            self.COMPRESSION_NONE,
        ]:
            raise ValueError(
                f"Unsupported compression level: {compression_level}")

        if compatibility_preset not in [
            "1.3",
            "1.4",
            "1.5",
            "1.6",
            "1.7",
        ]:
            raise ValueError(
                f"Unsupported compatibility level: {compatibility_preset}")

        # build command
        command = [
            f"{self._ghostscript_bin}",
            f"-dNOPAUSE",
            f"-dBATCH",
            f"-sDEVICE=pdfwrite",
            f"-dPDFSETTINGS=/{compression_level}",  # compression settings
            f"-dCompatibilityLevel={compatibility_preset}",  # PDF compatibility
            f"-sOutputFile={out_path}",
            f"{in_path}",
        ]

        logger.info(f"Executing Ghostscript ...")
        logger.debug(f"{" ".join(command)}")

        # Execute the FFmpeg command
        _convert_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        return _convert_process
