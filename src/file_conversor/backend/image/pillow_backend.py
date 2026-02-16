# src\file_conversor\backend\pillow_backend.py

"""
This module provides functionalities for handling image files using ``pillow`` backend.
"""

from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterable

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from PIL.ExifTags import TAGS

from file_conversor.backend.abstract_backend import AbstractBackend

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation


LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PillowBackend(AbstractBackend):
    """
    A class that provides an interface for handling image files using ``pillow``.
    """
    class AntialiasAlgorithm(Enum):
        MEDIAN = "median"
        MODE = "mode"

        def get(self):
            match self:
                case PillowBackend.AntialiasAlgorithm.MEDIAN:
                    return ImageFilter.MedianFilter
                case PillowBackend.AntialiasAlgorithm.MODE:
                    return ImageFilter.ModeFilter

    class PillowFilter(Enum):
        BLUR = "blur"
        SMOOTH = "smooth"
        SMOOTH_MORE = "smooth_more"
        SHARPEN = "sharpen"
        SHARPEN_MORE = "sharpen_more"
        EDGE_ENHANCE = "edge_enhance"
        EDGE_ENHANCE_MORE = "edge_enhance_more"
        EMBOSS = "emboss"
        EMBOSS_EDGE = "emboss_edge"

        def get(self) -> type[ImageFilter.Filter]:
            match self:
                case PillowBackend.PillowFilter.BLUR:
                    return ImageFilter.BLUR

                case PillowBackend.PillowFilter.SMOOTH:
                    return ImageFilter.SMOOTH

                case PillowBackend.PillowFilter.SMOOTH_MORE:
                    return ImageFilter.SMOOTH_MORE

                case PillowBackend.PillowFilter.SHARPEN:
                    return ImageFilter.DETAIL

                case PillowBackend.PillowFilter.SHARPEN_MORE:
                    return ImageFilter.SHARPEN

                case PillowBackend.PillowFilter.EDGE_ENHANCE:
                    return ImageFilter.EDGE_ENHANCE

                case PillowBackend.PillowFilter.EDGE_ENHANCE_MORE:
                    return ImageFilter.EDGE_ENHANCE_MORE

                case PillowBackend.PillowFilter.EMBOSS:
                    return ImageFilter.EMBOSS

                case PillowBackend.PillowFilter.EMBOSS_EDGE:
                    return ImageFilter.CONTOUR

    class ResamplingOption(Enum):
        BICUBIC = "bicubic"
        BILINEAR = "bilinear"
        LANCZOS = "lanczos"
        NEAREST = "nearest"

        def get(self) -> Image.Resampling:
            match self:
                case PillowBackend.ResamplingOption.BICUBIC:
                    return Image.Resampling.BICUBIC
                case PillowBackend.ResamplingOption.BILINEAR:
                    return Image.Resampling.BILINEAR
                case PillowBackend.ResamplingOption.LANCZOS:
                    return Image.Resampling.LANCZOS
                case PillowBackend.ResamplingOption.NEAREST:
                    return Image.Resampling.NEAREST

    class MirrorAxis(Enum):
        X = "x"
        Y = "y"

        def get(self) -> Callable[[Image.Image], Image.Image]:
            match self:
                case PillowBackend.MirrorAxis.X:
                    return ImageOps.mirror
                case PillowBackend.MirrorAxis.Y:
                    return ImageOps.flip

    Exif = Image.Exif
    Exif_TAGS = TAGS

    class SupportedInFormats(Enum):
        BMP = "bmp"
        GIF = "gif"
        ICO = "ico"
        JFIF = "jfif"
        JPG = "jpg"
        JPEG = "jpeg"
        JPE = "jpe"
        PNG = "png"
        PSD = "psd"
        TIF = "tif"
        TIFF = "tiff"
        WEBP = "webp"

    class SupportedOutFormats(Enum):
        BMP = "bmp"
        GIF = "gif"
        ICO = "ico"
        JPG = "jpg"
        APNG = "apng"
        PNG = "png"
        PDF = "pdf"
        TIF = "tif"
        WEBP = "webp"

        @property
        def format(self) -> str:
            match self:
                case PillowBackend.SupportedOutFormats.BMP:
                    return "BMP"
                case PillowBackend.SupportedOutFormats.GIF:
                    return "GIF"
                case PillowBackend.SupportedOutFormats.ICO:
                    return "ICO"
                case PillowBackend.SupportedOutFormats.JPG:
                    return "JPEG"
                case PillowBackend.SupportedOutFormats.APNG | PillowBackend.SupportedOutFormats.PNG:
                    return "PNG"
                case PillowBackend.SupportedOutFormats.PDF:
                    return "PDF"
                case PillowBackend.SupportedOutFormats.TIF:
                    return "TIFF"
                case PillowBackend.SupportedOutFormats.WEBP:
                    return "WEBP"

    EXTERNAL_DEPENDENCIES: set[str] = set()

    def __init__(self, verbose: bool = False,):
        """
        Initialize the ``pillow`` backend

        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__()
        self._verbose = verbose

    def info(self, input_file: Path) -> Exif:
        """
        Get EXIF info from input file.

        :param input_file: Input image file.
        """
        img = self._open(input_file)
        return img.getexif()

    def resize(self,
               output_file: Path,
               input_file: Path,
               width: int | None,
               scale: float | None = None,
               resampling: ResamplingOption = ResamplingOption.BICUBIC,
               ):
        """
        Resize input file.

        :param output_file: Output image file.
        :param input_file: Input image file.
        :param width: Width in pixels.
        :param scale: Scale image in proportion. Must be >0 (if used).
        :param resampling: Resampling algorithm used.
        """
        with self._open(input_file) as img:
            width = int(scale * img.width) if scale is not None else width

            if not width:
                raise ValueError(_("Cannot calculate width to resize the image"))

            height = int(width * float(img.height) / img.width)

            img_processed = img.resize(
                size=(width, height),
                resample=resampling.get()
            )
            self._save(
                img_processed,
                output_file,
            )

    def convert(
        self,
        output_file: Path,
        input_file: Path,
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
        """
        img = self._open(input_file)
        self._save(
            img,
            output_file,
            quality=quality,
            optimize=optimize,
        )

    def rotate(
        self,
        output_file: Path,
        input_file: Path,
        rotate: int,
        resampling: ResamplingOption = ResamplingOption.BICUBIC,
    ):
        """
        Rotate input file by X degrees (clockwise).

        :param output_file: Output image file.
        :param input_file: Input image file.
        :param rotate: Rotation degrees (-360-360).
        :param resampling: Resampling algorithm used.
        """
        # parse rotation argument
        img = self._open(input_file)
        img = img.rotate(-rotate, resample=resampling.get(), expand=True)  # clockwise rotation
        self._save(
            img,
            output_file,
        )

    def mirror(self, output_file: Path, input_file: Path, axis: MirrorAxis):
        """
        Mirror input file in relation X or Y axis.

        :param output_file: Output image file.
        :param input_file: Input image file.
        :param axis: Mirror in relation to x or y axis. 
        """
        img = self._open(input_file)

        transform_callback = axis.get()
        img = transform_callback(img)

        self._save(
            img,
            output_file,
        )

    def blur(
        self,
        output_file: Path,
        input_file: Path,
        blur_pixels: int,
    ):
        """
        Blurs an input image file using GaussianBlur.

        :param output_file: Output image file.
        :param input_file: Input image file.        
        :param blur_pixels: Blur radius (in pixels). Higher number = more blur.        
        """
        img = self._open(input_file)
        img = img.filter(
            ImageFilter.GaussianBlur(radius=blur_pixels)
        )
        self._save(
            img,
            output_file,
        )

    def unsharp_mask(
        self,
        output_file: Path,
        input_file: Path,
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
        """
        img = self._open(input_file)
        img = img.filter(ImageFilter.UnsharpMask(
            radius=radius,
            percent=percent,
            threshold=threshold,
        ))
        self._save(
            img,
            output_file,
        )

    def antialias(
        self,
        output_file: Path,
        input_file: Path,
        radius: int,
        algorithm: AntialiasAlgorithm = AntialiasAlgorithm.MEDIAN,
    ):
        """
        Applies antialias to an input image file using Median or Mode algorithms.

        :param output_file: Output image file.
        :param input_file: Input image file.        

        :param radius: Box radius (kernel size) to calculate pixel averaging.
        :param algorithm: Algorithm used. Available options are "median" (default, replaces each pixel with the median of its neighbors), "mode" (replaces each pixel with the most common (mode) pixel value in the neighborhood).
        """
        img = self._open(input_file)

        filter_algo = algorithm.get()
        img = img.filter(filter_algo(radius))

        self._save(
            img,
            output_file,
        )

    def enhance(
        self,
        output_file: Path,
        input_file: Path,
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


        """
        img = self._open(input_file)
        img = ImageEnhance.Color(img).enhance(color_factor)
        img = ImageEnhance.Contrast(img).enhance(contrast_factor)
        img = ImageEnhance.Brightness(img).enhance(brightness_factor)
        img = ImageEnhance.Sharpness(img).enhance(sharpness_factor)
        self._save(
            img,
            output_file,
        )

    def filter(
        self,
        output_file: Path,
        input_file: Path,
        filters: Iterable[PillowFilter],
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
        """
        img = self._open(input_file)
        for filter in filters:
            img = img.filter(filter.get())
        self._save(
            img,
            output_file,
        )

    def _open(self, input_file: Path | str):
        img = Image.open(input_file)
        # 1. Transparency -> convert to RGBA
        if img.mode == "P" and "transparency" in img.info:
            img = img.convert("RGBA")
        return img

    def _save(
        self,
        img: Image.Image,
        output_file: Path,
        quality: int = 90,
        optimize: bool = True,
    ):
        """
        Corrects common errors in images and saves them.

        :param img: Image to be corrected.
        :param output_file: File to save img.        
        :param quality: Quality of the saved image (if applicable).
        :param optimize: Whether to optimize the saved image (if applicable).

        :raises Exception: if image correction fails.
        """
        output_file = Path(output_file).resolve()
        output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext = output_file.suffix[1:]
        file_format = self.SupportedOutFormats(out_ext).format

        # save parameters
        params: dict[str, Any] = {
            "quality": quality,
            "optimize": optimize,
            "lossless": quality == 100,  # valid only for WEBP
        }

        try:
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

            elif (
                file_format == "TIFF" and img.mode not in ("RGB", "RGBA", "L")
            ) or (
                file_format == "BMP" and img.mode not in ("RGB",)
            ):
                img = img.convert("RGB")

        except Exception as e:
            logger.error(f"{_('Image correction failed')}: {e}")
            raise

        # save image
        img.save(
            output_file,
            format=file_format,
            **params,
        )


__all__ = [
    "PillowBackend",
]
