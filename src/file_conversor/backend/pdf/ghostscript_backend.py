# src\file_conversor\backend\ghostscript_backend.py

"""
This module provides functionalities for handling files using ``ghostscript`` backend.
"""

import re

from pathlib import Path

from enum import Enum
from typing import Any, Callable

# user-provided imports
from file_conversor.config import Environment, Log
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
    class OutputFileFormat(Enum):
        PDF = "pdf"

        def get(self):
            if self.value == "pdf":
                return "pdfwrite"
            raise ValueError(f"Unsupported output file format: {self.value}")

        def get_options(self) -> list[str]:
            return [f"-sDEVICE={self.get()}"]

    class Compression(Enum):
        HIGH = "high"
        """72 dpi quality - high compression / low quality"""
        MEDIUM = "medium"
        """150 dpi quality - medium compression / medium quality"""
        LOW = "low"
        """300 dpi quality - low compression / high quality"""
        NONE = "none"
        """600 dpi quality - no compression / highest quality"""

        def get(self):
            if self.value == "high":
                return "screen"
            if self.value == "medium":
                return "ebook"
            if self.value == "low":
                return "printer"
            if self.value == "none":
                return "prepress"
            raise ValueError(f"Unsupported compression level: {self.value}")

        def get_options(self) -> list[str]:
            return [f"-dPDFSETTINGS=/{self.get()}"]

    class CompatibilityPreset(Enum):
        PRESET_1_3 = "1.3"
        """legacy option"""
        PRESET_1_4 = "1.4"
        """legacy option"""
        PRESET_1_5 = "1.5"
        """good campatibility / support for object stream compression"""
        PRESET_1_6 = "1.6"
        """medium campatibility / support for JPEG2000 compression"""
        PRESET_1_7 = "1.7"
        """low campatibility / support for 3D and transparency"""

        def get(self):
            if self.value == "1.3":
                return "1.3"
            if self.value == "1.4":
                return "1.4"
            if self.value == "1.5":
                return "1.5"
            if self.value == "1.6":
                return "1.6"
            if self.value == "1.7":
                return "1.7"
            raise ValueError(f"Unsupported compatibility preset: {self.value}")

        def get_options(self) -> list[str]:
            return [f"-dCompatibilityLevel={self.get()}"]  # PDF preset

    class Downsampling(Enum):
        HIGH = "high"
        """slowest processing / highest quality"""
        MEDIUM = "medium"
        """medium processing / medium quality"""
        LOW = "low"
        """fast processing / low quality"""

        def get(self):
            if self.value == "high":
                return "Bicubic"
            if self.value == "medium":
                return "Average"
            if self.value == "low":
                return "Subsample"
            raise ValueError(f"Unsupported downsampling type: {self.value}")

        def get_options(self) -> list[str]:
            value = self.get()
            return [
                f"-dDownsampleColorImages=true",
                f"-dDownsampleGrayImages=true",
                f"-dColorImageDownsampleType=/{value}",
                f"-dGrayImageDownsampleType=/{value}",
            ]

    class ImageCompression(Enum):
        JPX = "jpx"
        """JPEG2000 format (poor support by browsers / open source viewers)"""
        JPG = "jpg"
        """JPEG format (great support by browsers / open source viewers)"""
        PNG = "png"
        """PNG format (great support / high file size)"""

        def get(self):
            if self.value == "jpx":
                return "JPXEncode"
            if self.value == "jpg":
                return "DCTEncode"
            if self.value == "png":
                return "FlateEncode"
            raise ValueError(f"Unsupported image compression format: {self.value}")

        def get_options(self) -> list[str]:
            value = self.get()
            return [
                f"-dAutoFilterColorImages=false",
                f"-dAutoFilterGrayImages=false",
                f"-dColorImageFilter=/{value}",
                f"-dGrayImageFilter=/{value}",
            ]

    class JPEGCompression(Enum):
        NONE = "none"
        """no compression / highest quality"""
        LOW = "low"
        """low compression / high quality"""
        MEDIUM = "medium"
        """medium compression / medium quality"""
        HIGH = "high"
        """high compression / low quality"""

        def get(self):
            if self.value == "none":
                return 99
            if self.value == "low":
                return 90
            if self.value == "medium":
                return 80
            if self.value == "high":
                return 70
            raise ValueError(f"Unsupported JPEG compression level: {self.value}")

        def get_options(self) -> list[str]:
            return [
                f"-dJPEGQ={self.get()}",
            ]

    SUPPORTED_IN_FORMATS = {
        "pdf": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "pdf": {
            "out_file_format": OutputFileFormat.PDF,
        },
    }
    EXTERNAL_DEPENDENCIES = {
        "gs",
    }

    def __init__(
        self,
        install_deps: bool | None,
        verbose: bool = False,
    ):
        """
        Initialize the backend.

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action. 

        :raises RuntimeError: if dependency is not found
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

    def _get_gs_command(self) -> list[str]:
        """
        Get the base Ghostscript command.

        :return: List of Ghostscript command and basic options.
        """
        return [
            f"{self._ghostscript_bin}",
            # set non-interactive mode
            f"-dNOPAUSE",
            f"-dBATCH",
        ]

    def _get_inout_options(self, in_path: Path, out_path: Path) -> list[str]:
        """
        Get input/output options for Ghostscript command.

        :param in_path: Input file path.
        :param out_path: Output file path.
        :return: List of input/output options.
        """
        return [
            f"-sOutputFile={out_path}",
            f"{in_path}",
        ]

    def _get_num_pages(self, line: str) -> int | None:
        """
        Get number of pages from Ghostscript output line.

        :param line: Ghostscript output line.
        :return: Number of pages or None if not found.
        """
        match = re.search(r'Processing pages (\d+) through (\d+)', line)
        if not match:
            return None
        begin = int(match.group(1))
        end = int(match.group(2))
        num_pages = end - begin + 1
        return num_pages

    def _get_progress(self, num_pages: int, line: str) -> float | None:
        """
        Get progress percentage from Ghostscript output line.

        :param num_pages: Total number of pages.
        :param line: Ghostscript output line.
        :return: Progress percentage or None if not found.
        """
        match = re.search(r'Page\s*(\d+)', line)
        if not match:
            return None
        pages = int(match.group(1))
        progress = 100.0 * (float(pages) / num_pages)
        return progress

    def compress(self,
                 output_file: str | Path,
                 input_file: str | Path,
                 compression_level: Compression,
                 compatibility_preset: CompatibilityPreset = CompatibilityPreset.PRESET_1_5,
                 downsampling_type: Downsampling = Downsampling.HIGH,
                 image_compression: ImageCompression = ImageCompression.JPG,
                 progress_callback: Callable[[float], Any] | None = None,
                 ):
        """
        Compress input PDF files.

        :param output_file: Output file
        :param input_file: Input file.         
        :param compression_level: Compression level.
        :param compatibility_level: PDF compatibility level (1.3 - 1.7). Defaults to ``CompatibilityPreset.PRESET_1_5`` (good compatibility / stream compression support).
        :param downsampling_type: Image downsampling type. Defaults to ``Downsampling.HIGH`` (best image quality / slower processing).
        :param image_compression: Image compression format. Defaults to `ImageCompression.JPG` (great compatibility / good compression).
        :param progress_callback: Progress callback (0-100). Defaults to None.

        :raises FileNotFoundError: if input file not found
        :raises ValueError: if output format is unsupported
        """
        self.check_file_exists(input_file)
        in_path = Path(input_file)

        out_path = Path(output_file)
        out_path = out_path.with_suffix(out_path.suffix.lower())

        out_ext = out_path.suffix[1:]
        if out_ext not in self.SUPPORTED_OUT_FORMATS:
            raise ValueError(f"Output format '{out_ext}' not supported")

        out_file_format: GhostscriptBackend.OutputFileFormat = self.SUPPORTED_OUT_FORMATS[out_ext]["out_file_format"]

        # build command
        command = self._get_gs_command()

        # add options
        command.extend(out_file_format.get_options())  # file_device options
        command.extend(compression_level.get_options())  # compression options
        command.extend(compatibility_preset.get_options())  # compatibility options
        command.extend(downsampling_type.get_options())  # downsampling options
        command.extend(image_compression.get_options())  # set image compression

        # adjust JPEG compression if needed
        if image_compression == GhostscriptBackend.ImageCompression.JPG:
            compression_level_name = compression_level.name.upper()
            jpeg_compression = GhostscriptBackend.JPEGCompression[compression_level_name]
            command.extend(jpeg_compression.get_options())  # set JPEG compression

        # set input/output files
        command.extend(self._get_inout_options(in_path, out_path))

        # Execute the FFmpeg command
        process = Environment.run_nowait(
            *command,
        )

        # process output
        out_lines: list[str] = []
        num_pages: int = 0
        progress: float = 0.0
        while process.poll() is None:
            if not process.stdout:
                continue
            line = process.stdout.readline()
            out_lines.append(line)  # collect output lines for error checking

            num_pages = self._get_num_pages(line) or num_pages
            progress = self._get_progress(num_pages, line) or progress

            if progress_callback:
                progress_callback(progress)

        Environment.check_returncode(process, out_lines=out_lines)
        return process


__all__ = [
    "GhostscriptBackend",
]
