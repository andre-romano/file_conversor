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
        PDF = "pdfwrite"

        @classmethod
        def get_dict(cls):
            return {
                "pdf": cls.PDF,
            }

        @classmethod
        def from_str(cls, name: str):
            return cls.get_dict()[name]

        def get_options(self) -> list[str]:
            return [f"-sDEVICE={self.value}"]

    class Compression(Enum):
        HIGH = "screen"
        """72 dpi quality - high compression / low quality"""
        MEDIUM = "ebook"
        """150 dpi quality - medium compression / medium quality"""
        LOW = "printer"
        """300 dpi quality - low compression / high quality"""
        NONE = "preprint"
        """600 dpi quality - no compression / highest quality"""

        @classmethod
        def get_dict(cls):
            return {
                "high": cls.HIGH,
                "medium": cls.MEDIUM,
                "low": cls.LOW,
                "none": cls.NONE,
            }

        @classmethod
        def from_str(cls, name: str):
            return cls.get_dict()[name]

        def get_options(self) -> list[str]:
            return [f"-dPDFSETTINGS=/{self.value}"]

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

        @classmethod
        def get_dict(cls):
            return {
                "1.3": cls.PRESET_1_3,
                "1.4": cls.PRESET_1_4,
                "1.5": cls.PRESET_1_5,
                "1.6": cls.PRESET_1_6,
                "1.7": cls.PRESET_1_7,
            }

        @classmethod
        def from_str(cls, name: str):
            return cls.get_dict()[name]

        def get_options(self) -> list[str]:
            return [f"-dCompatibilityLevel={self.value}"]  # PDF preset

    class Downsampling(Enum):
        HIGH = "Bicubic"
        """slowest processing / highest quality"""
        MEDIUM = "Average"
        """medium processing / medium quality"""
        LOW = "Subsample"
        """fast processing / low quality"""

        @classmethod
        def get_dict(cls):
            return {
                "high": cls.HIGH,
                "medium": cls.MEDIUM,
                "low": cls.LOW,
            }

        @classmethod
        def from_str(cls, name: str):
            return cls.get_dict()[name]

        def get_options(self) -> list[str]:
            return [
                f"-dDownsampleColorImages=true",
                f"-dDownsampleGrayImages=true",
                f"-dColorImageDownsampleType=/{self.value}",
                f"-dGrayImageDownsampleType=/{self.value}",
            ]

    class ImageCompression(Enum):
        JPX = "JPXEncode"
        """JPEG2000 format (poor support by browsers / open source viewers)"""
        JPG = "DCTEncode"
        """JPEG format (great support by browsers / open source viewers)"""
        PNG = "FlateEncode"
        """PNG format (great support / high file size)"""

        @classmethod
        def get_dict(cls):
            return {
                "jpx": cls.JPX,
                "jpg": cls.JPG,
                "png": cls.PNG,
            }

        @classmethod
        def from_str(cls, name: str):
            return cls.get_dict()[name]

        def get_options(self) -> list[str]:
            return [
                f"-dAutoFilterColorImages=false",
                f"-dAutoFilterGrayImages=false",
                f"-dColorImageFilter=/{self.value}",
                f"-dGrayImageFilter=/{self.value}",
            ]

    class JPEGCompression(Enum):
        NONE = 99
        """no compression / highest quality"""
        LOW = 90
        """low compression / high quality"""
        MEDIUM = 80
        """medium compression / medium quality"""
        HIGH = 70
        """high compression / low quality"""

        @classmethod
        def get_dict(cls):
            return {
                "none": cls.NONE,
                "low": cls.LOW,
                "medium": cls.MEDIUM,
                "high": cls.HIGH,
            }

        @classmethod
        def from_str(cls, name: str):
            return cls.get_dict()[name]

        def get_options(self) -> list[str]:
            return [
                f"-dJPEGQ={self.value}",
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
            compression_level_name = compression_level.name.lower()
            jpeg_compression = GhostscriptBackend.JPEGCompression.from_str(compression_level_name)
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
