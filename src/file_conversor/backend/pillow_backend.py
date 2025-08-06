# src\file_conversor\backend\pillow_backend.py

"""
This module provides functionalities for handling image files using ``pillow`` backend.
"""

from PIL import Image, ImageOps
from PIL.ExifTags import TAGS

# user-provided imports
from file_conversor.config.locale import get_translation
from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.utils.file import File

_ = get_translation()


class PillowBackend(AbstractBackend):
    """
    A class that provides an interface for handling image files using ``pillow``.
    """

    Exif = Image.Exif
    Exif_TAGS = TAGS

    SUPPORTED_IN_FORMATS = {
        "bmp": {},
        "gif": {},
        "ico": {},
        "jfif": {},
        "jpg": {},
        "jpeg": {},
        "jpe": {},
        "png": {},
        "psd": {},
        "tif": {},
        "tiff": {},
        "webp": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "bmp": {"format": "BMP"},
        "gif": {"format": "GIF"},
        "ico": {"format": "ICO"},
        "jpg": {"format": "JPEG"},
        "apng": {"format": "PNG"},
        "png": {"format": "PNG"},
        "pdf": {"format": "PDF"},
        "tif": {"format": "TIFF"},
        "webp": {"format": "WEBP"},
    }

    def __init__(self, verbose: bool = False,):
        """
        Initialize the ``pillow`` backend

        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__()
        self._verbose = verbose

    def info(self, input_file: str,) -> Exif:
        """
        Get EXIF info from input file.

        :param input_file: Input image file.

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        img = Image.open(input_file)
        return img.getexif()

    def convert(
        self,
        output_file: str,
        input_file: str,
        quality: int = 90,
        optimize: bool = True,
    ):
        """
        Convert input file into an output.

        :param output_file: Output image file.
        :param input_file: Input image file.
        :param quality: Final quality of image file (1-100). If 100, activates lossless compression. Valid only for JPG, WEBP out formats. Defaults to 90.
        :param optimize: Improve file size, without losing quality (lossless compression). Valid only for JPG, PNG, WEBP out formats Defaults to True.

        :raises ValueError: invalid quality value. Valid values are 1-100.
        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)
        if quality < 1 or quality > 100:
            raise ValueError(f"{_('Invalid quality level. Valid values are')} 1-100.")

        out_file = File(output_file)
        format = self.SUPPORTED_OUT_FORMATS[out_file.get_extension()]["format"]

        img = Image.open(input_file)
        img.save(output_file,
                 format=format,
                 quality=quality,
                 optimize=optimize,
                 lossless=True if quality == 100 else False,  # valid only for WEBP
                 )

    def rotate(self, output_file: str, input_file: str, rotate: int):
        """
        Rotate input file by X degrees.

        :param output_file: Output image file.
        :param input_file: Input image file.
        :param rotate: Rotation degrees (0-360).

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        out_file = File(output_file)
        format = self.SUPPORTED_OUT_FORMATS[out_file.get_extension()]["format"]

        img = Image.open(input_file)
        img = img.rotate(rotate)
        img.save(
            output_file,
            format=format,
            quality=90,
            optimize=True,
        )

    def mirror(self, output_file: str, input_file: str, x_y: bool):
        """
        Mirror input file in relation X or Y axis.

        :param output_file: Output image file.
        :param input_file: Input image file.
        :param x_y: Mirror in relation to x or y axis. True for X axis (mirror image horizontally). False for Y axis (flip image vertically).

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        out_file = File(output_file)
        format = self.SUPPORTED_OUT_FORMATS[out_file.get_extension()]["format"]

        img = Image.open(input_file)
        if x_y:
            img = ImageOps.mirror(img)
        else:
            img = ImageOps.flip(img)
        img.save(
            output_file,
            format=format,
            quality=90,
            optimize=True,
        )
