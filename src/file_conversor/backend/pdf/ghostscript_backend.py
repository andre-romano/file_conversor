# src\file_conversor\backend\ghostscript_backend.py

"""
This module provides functionalities for handling files using ``ghostscript`` backend.
"""

from pathlib import Path
from enum import Enum
from typing import Any

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

        def get_options(self) -> list[str]:
            return [f"-dCompatibilityLevel={self.value}"]  # PDF preset

    class Downsampling(Enum):
        HIGH = "Bicubic"
        """slowest processing / highest quality"""
        MEDIUM = "Average"
        """medium processing / medium quality"""
        LOW = "Subsample"
        """fast processing / low quality"""

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

        def get_options(self) -> list[str]:
            return [
                f"-dAutoFilterColorImages=false",
                f"-dAutoFilterGrayImages=false",
                f"-dColorImageFilter=/{self.value}",
                f"-dGrayImageFilter=/{self.value}",
            ]

    SUPPORTED_IN_FORMATS = {
        "pdf": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "pdf": {
            "out_file_format": OutputFileFormat.PDF,
        },
    }

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
                 compression_level: Compression,
                 compatibility_preset: CompatibilityPreset = CompatibilityPreset.PRESET_1_5,
                 downsampling_type: Downsampling = Downsampling.HIGH,
                 image_compression: ImageCompression = ImageCompression.JPG,
                 ):
        """
        Compress input PDF files.

        :param output_file: Output file
        :param input_file: Input file.         
        :param compression_level: Compression level.
        :param compatibility_level: PDF compatibility level (1.3 - 1.7). Defaults to ``CompatibilityPreset.PRESET_1_5`` (good compatibility / stream compression support).
        :param downsampling_type: Image downsampling type. Defaults to ``Downsampling.HIGH`` (best image quality / slower processing).
        :param image_compression: Image compression format. Defaults to `ImageCompression.JPG` (great compatibility / good compression).

        :raises FileNotFoundError: if input file not found
        :raises ValueError: if output format is unsupported
        """
        self.check_file_exists(input_file)
        in_path = Path(input_file)
        out_path = Path(output_file)

        out_ext = out_path.suffix[1:]
        if out_ext not in self.SUPPORTED_OUT_FORMATS:
            raise ValueError(f"Output format '{out_ext}' not supported")

        out_file_format: GhostscriptBackend.OutputFileFormat = self.SUPPORTED_OUT_FORMATS[out_ext]["out_file_format"]

        # build command
        command = [
            f"{self._ghostscript_bin}",

            # set non-interactive mode
            f"-dNOPAUSE",
            f"-dBATCH",
        ]

        command.extend(out_file_format.get_options())  # file_device options
        command.extend(compression_level.get_options())  # compression options
        command.extend(compatibility_preset.get_options())  # compatibility options
        command.extend(downsampling_type.get_options())  # downsampling options
        command.extend(image_compression.get_options())  # set image compression
        if image_compression == GhostscriptBackend.ImageCompression.JPG:
            if compression_level == GhostscriptBackend.Compression.HIGH:
                command.append(f"-dJPEGQ=70")  # Set JPEG quality
            elif compression_level == GhostscriptBackend.Compression.MEDIUM:
                command.append(f"-dJPEGQ=80")  # Set JPEG quality
            elif compression_level == GhostscriptBackend.Compression.LOW:
                command.append(f"-dJPEGQ=90")  # Set JPEG quality
            else:
                command.append(f"-dJPEGQ=99")  # Set JPEG quality

        # set input/output files
        command.extend([
            f"-sOutputFile={out_path}",
            f"{in_path}",
        ])

        logger.info(f"Executing Ghostscript ...")
        logger.debug(f"{" ".join(command)}")

        # Execute the FFmpeg command
        process = Environment.run(
            *command,
        )
        return process
