# src\file_conversor\backend\pillow_backend.py

"""
This module provides functionalities for handling image files using ``pillow`` backend.
"""

from enum import Enum
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from PIL.ExifTags import TAGS

from pathlib import Path

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.formatters import normalize_degree
from file_conversor.utils.validators import is_close

from file_conversor.backend.abstract_backend import AbstractBackend

LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PillowBackend(AbstractBackend):
    """
    A class that provides an interface for handling image files using ``pillow``.
    """
    class AntialiasAlgorithm(Enum):
        MEDIAN = ImageFilter.MedianFilter
        MODE = ImageFilter.ModeFilter

        @classmethod
        def from_str(cls, name: str):
            name = name.lower()
            return cls.get_dict()[name]

        @classmethod
        def get_dict(cls):
            return {
                "median": cls.MEDIAN,
                "mode": cls.MODE,
            }

    PILLOW_FILTERS: dict[str, type[ImageFilter.BuiltinFilter]] = {
        "blur": ImageFilter.BLUR,
        "smooth": ImageFilter.SMOOTH,
        "smooth_more": ImageFilter.SMOOTH_MORE,
        "sharpen": ImageFilter.DETAIL,
        "sharpen_more": ImageFilter.SHARPEN,
        "edge_enhance": ImageFilter.EDGE_ENHANCE,
        "edge_enhance_more": ImageFilter.EDGE_ENHANCE_MORE,
        "emboss": ImageFilter.EMBOSS,
        "emboss_edge": ImageFilter.CONTOUR,
    }

    Exif = Image.Exif
    Exif_TAGS = TAGS

    RESAMPLING_OPTIONS = {
        "bicubic": Image.Resampling.BICUBIC,
        "bilinear": Image.Resampling.BILINEAR,
        "lanczos": Image.Resampling.LANCZOS,
        "nearest": Image.Resampling.NEAREST,
    }

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
    EXTERNAL_DEPENDENCIES: set[str] = set()

    def __init__(self, verbose: bool = False,):
        """
        Initialize the ``pillow`` backend

        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__()
        self._verbose = verbose

    def info(self, input_file: str | Path,) -> Exif:
        """
        Get EXIF info from input file.

        :param input_file: Input image file.

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        img = self._open(input_file)
        return img.getexif()

    def resize(self,
               output_file: str | Path,
               input_file: str | Path,
               width: int | None,
               scale: float | None = None,
               resampling: Image.Resampling = Image.Resampling.BICUBIC,
               ):
        """
        Resize input file.

        :param output_file: Output image file.
        :param input_file: Input image file.
        :param width: Width in pixels.
        :param scale: Scale image in proportion. Must be >0 (if used).
        :param resampling: Resampling algorithm used.

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        output_file = Path(output_file).resolve()
        output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext = output_file.suffix[1:]
        file_format = self.SUPPORTED_OUT_FORMATS[out_ext]["format"]

        with self._open(input_file) as img:
            if scale:
                if scale <= 0:
                    raise RuntimeError(_("Scale must be >0"))
                width = int(scale * img.width)
            if not width:
                raise RuntimeError(_("Need either scale or width to resize an image"))
            if width <= 0:
                raise RuntimeError(_("Width must be > 0"))
            height = int(width * float(img.height) / img.width)

            img = img.resize(
                size=(width, height),
                resample=resampling
            )
            self._save(
                img,
                output_file,
                file_format=file_format,
                quality=90,
                optimize=True,
            )

    def convert(
        self,
        output_file: str | Path,
        input_file: str | Path,
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

        output_file = Path(output_file).resolve()
        output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext = output_file.suffix[1:]

        file_format = self.SUPPORTED_OUT_FORMATS[out_ext]["format"]

        img = self._open(input_file)
        self._save(
            img,
            output_file,
            file_format=file_format,
            quality=quality,
            optimize=optimize,
            lossless=True if is_close(quality, 100) else False,  # valid only for WEBP
        )

    def rotate(
        self,
        output_file: str | Path,
        input_file: str | Path,
        rotate: int,
        resampling: Image.Resampling = Image.Resampling.BICUBIC,
    ):
        """
        Rotate input file by X degrees (clockwise).

        :param output_file: Output image file.
        :param input_file: Input image file.
        :param rotate: Rotation degrees (-360-360).
        :param resampling: Resampling algorithm used.

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        # parse rotation argument
        rotate = normalize_degree(rotate)

        output_file = Path(output_file).resolve()
        output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext = output_file.suffix[1:]

        file_format = self.SUPPORTED_OUT_FORMATS[out_ext]["format"]

        img = self._open(input_file)
        img = img.rotate(-rotate, resample=resampling, expand=True)  # clockwise rotation
        self._save(
            img,
            output_file,
            file_format=file_format,
            quality=90,
            optimize=True,
        )

    def mirror(self, output_file: str | Path, input_file: str | Path, x_y: bool):
        """
        Mirror input file in relation X or Y axis.

        :param output_file: Output image file.
        :param input_file: Input image file.
        :param x_y: Mirror in relation to x or y axis. True for X axis (mirror image horizontally). False for Y axis (flip image vertically).

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        output_file = Path(output_file).resolve()
        output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext = output_file.suffix[1:]
        file_format = self.SUPPORTED_OUT_FORMATS[out_ext]["format"]

        img = self._open(input_file)
        if x_y:
            img = ImageOps.mirror(img)
        else:
            img = ImageOps.flip(img)
        self._save(
            img,
            output_file,
            file_format=file_format,
            quality=90,
            optimize=True,
        )

    def blur(
        self,
        output_file: str | Path,
        input_file: str | Path,
        blur_pixels: int,
    ):
        """
        Blurs an input image file using GaussianBlur.

        :param output_file: Output image file.
        :param input_file: Input image file.        
        :param blur_pixels: Blur radius (in pixels). Higher number = more blur.        

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        output_file = Path(output_file).resolve()
        output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext = output_file.suffix[1:]

        file_format = self.SUPPORTED_OUT_FORMATS[out_ext]["format"]

        img = self._open(input_file)
        img = img.filter(
            ImageFilter.GaussianBlur(radius=blur_pixels)
        )
        self._save(
            img,
            output_file,
            file_format=file_format,
            quality=90,
            optimize=True,
        )

    def unsharp_mask(
        self,
        output_file: str | Path,
        input_file: str | Path,
        radius: float,
        percent: int,
        threshold: int,
    ):
        """
        Sharpens an input image file using unsharp mask.

        :param output_file: Output image file.
        :param input_file: Input image file.        

        :param radius: Pixels to blur.
        :param percent: Strength of sharpening.
        :param threshold: How different pixels must be from neighbors to be sharpened (controls noise amplification).

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        output_file = Path(output_file).resolve()
        output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext = output_file.suffix[1:]
        file_format = self.SUPPORTED_OUT_FORMATS[out_ext]["format"]

        img = self._open(input_file)
        img = img.filter(ImageFilter.UnsharpMask(
            radius=radius,
            percent=percent,
            threshold=threshold,
        ))
        self._save(
            img,
            output_file,
            file_format=file_format,
            quality=90,
            optimize=True,
        )

    def antialias(
        self,
        output_file: str | Path,
        input_file: str | Path,
        radius: int,
        algorithm: AntialiasAlgorithm = AntialiasAlgorithm.MEDIAN,
    ):
        """
        Applies antialias to an input image file using Median or Mode algorithms.

        :param output_file: Output image file.
        :param input_file: Input image file.        

        :param radius: Box radius (kernel size) to calculate pixel averaging.
        :param algorithm: Algorithm used. Available options are "median" (default, replaces each pixel with the median of its neighbors), "mode" (replaces each pixel with the most common (mode) pixel value in the neighborhood).

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        output_file = Path(output_file).resolve()
        output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext = output_file.suffix[1:]
        file_format = self.SUPPORTED_OUT_FORMATS[out_ext]["format"]

        img = self._open(input_file)
        img = img.filter(algorithm.value(radius))
        self._save(
            img,
            output_file,
            file_format=file_format,
            quality=90,
            optimize=True,
        )

    def enhance(
        self,
        output_file: str | Path,
        input_file: str | Path,
        color_factor: float = 1.0,
        contrast_factor: float = 1.0,
        brightness_factor: float = 1.0,
        sharpness_factor: float = 1.0,
    ):
        """
        Enhances an input image file.

        :param output_file: Output image file.
        :param input_file: Input image file.        

        :param color_factor: 0.0 = black and white | 1.0 = original color | 2.0 very saturated
        :param contrast_factor: 0.0 = gray | 1.0 = original constrat | 2.0 strong contrast
        :param brightness_factor: 0.0 = black | 1.0 = original brightness | 2.0 very bright
        :param sharpness_factor: 0.0 = blurred | 1.0 = original | 2.0 sharpen edges

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        output_file = Path(output_file).resolve()
        output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext = output_file.suffix[1:]
        file_format = self.SUPPORTED_OUT_FORMATS[out_ext]["format"]

        img = self._open(input_file)
        img = ImageEnhance.Color(img).enhance(color_factor)
        img = ImageEnhance.Contrast(img).enhance(contrast_factor)
        img = ImageEnhance.Brightness(img).enhance(brightness_factor)
        img = ImageEnhance.Sharpness(img).enhance(sharpness_factor)
        self._save(
            img,
            output_file,
            file_format=file_format,
            quality=90,
            optimize=True,
        )

    def filter(
        self,
        output_file: str | Path,
        input_file: str | Path,
        filters: list[ImageFilter.BuiltinFilter] | list[str],
    ):
        """
        Enhances an input image file.

        :param output_file: Output image file.
        :param input_file: Input image file.        
        :param filters: Filters to apply in image. Check PillowFilter for supported filters.

        filters =

        - "blur": {_('Blurs image')}

        - "smooth": {_('Softens image, similar to blur')}

        - "smooth_more": {_('Softens image more')}

        - "sharpen": {_('Increase image sharpness')}

        - "sharpen_more": {_('Increase image sharpness - stronger sharpness')}

        - "edge_enhance": {_('Enhance edge contours of the image')}

        - "edge_enhance_more": {_('Enhance edge contours of the image - stronger enhancement')}

        - "edge_enhance_map": {_('Enhance edge contours of the image - use mapping algorithm')}

        - "emboss": {_('Create 3D emboss effect in the image')}

        - "emboss_draw": {_('Draw edge contours of the image')}

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        output_file = Path(output_file).resolve()
        output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext = output_file.suffix[1:]
        file_format = self.SUPPORTED_OUT_FORMATS[out_ext]["format"]

        img = self._open(input_file)
        for filter in filters:
            if isinstance(filter, str):
                img_filter = self.PILLOW_FILTERS[filter]
            img = img.filter(img_filter)
        self._save(
            img,
            output_file,
            file_format=file_format,
            quality=90,
            optimize=True,
        )

    def _open(self, input_file: Path | str):
        img = Image.open(input_file)
        # 1. Transparency -> convert to RGBA
        if img.mode == "P" and "transparency" in img.info:
            img = img.convert("RGBA")
        return img

    def _save(self, img: Image.Image, output_file: str | Path, file_format: str, **params):
        """
        Corrects common errors in images and saves them.

        :param img: Image to be corrected.
        :param output_file: File to save img.
        :param format: Target format to save img.
        :param params: Additional parameters for saving the image, such as quality and optimize.

        :raises Exception: if image correction fails.
        """
        try:
            file_format = file_format.upper()  # ensure uppercase format

            # 0. Preserve EXIF and ICC if they exist
            if "exif" in img.info and img.info["exif"]:
                params.setdefault("exif", img.info["exif"])
            if "icc_profile" in img.info and img.info["icc_profile"]:
                params.setdefault("icc_profile", img.info["icc_profile"])

            # 2. Convert incompatible modes to the target format
            if file_format in ("JPEG",) and img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            elif file_format in ("PNG", "WEBP") and img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")
            elif file_format == "TIFF" and img.mode not in ("RGB", "RGBA", "L"):
                img = img.convert("RGB")
            elif file_format == "BMP" and img.mode not in ("RGB",):
                img = img.convert("RGB")
        except Exception as e:
            logger.error(f"{_('Image correction failed')}: {e}")
            raise

        # save image
        img.save(output_file, format=file_format, **params)


__all__ = [
    "PillowBackend",
]
