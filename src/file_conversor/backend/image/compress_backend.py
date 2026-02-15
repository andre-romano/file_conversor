# src\file_conversor\backend\compress_backend.py

from enum import Enum
from pathlib import Path
from typing import Any

from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.backend.image._gifsicle_backend import GifSicleBackend
from file_conversor.backend.image._mozjpeg_backend import MozJPEGBackend
from file_conversor.backend.image._oxipng_backend import OxiPNGBackend

# user-provided imports
from file_conversor.config import Log, get_translation


_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class CompressBackend(AbstractBackend):
    """
    Provides an interface for handling image file compression using multiple backends.
    """

    class SupportedInFormats(Enum):
        GIF = GifSicleBackend.SupportedInFormats.GIF.value
        JPG = MozJPEGBackend.SupportedInFormats.JPG.value
        JPEG = MozJPEGBackend.SupportedInFormats.JPEG.value
        PNG = OxiPNGBackend.SupportedInFormats.PNG.value

        @property
        def backend(self) -> type[GifSicleBackend | MozJPEGBackend | OxiPNGBackend]:
            match self:
                case CompressBackend.SupportedInFormats.GIF:
                    return GifSicleBackend
                case CompressBackend.SupportedInFormats.JPG | CompressBackend.SupportedInFormats.JPEG:
                    return MozJPEGBackend
                case CompressBackend.SupportedInFormats.PNG:
                    return OxiPNGBackend

    SupportedOutFormats = SupportedInFormats

    EXTERNAL_DEPENDENCIES = {
        *GifSicleBackend.EXTERNAL_DEPENDENCIES,
        *MozJPEGBackend.EXTERNAL_DEPENDENCIES,
        *OxiPNGBackend.EXTERNAL_DEPENDENCIES,
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
        super().__init__()
        # get required dependencies
        for mode in CompressBackend.SupportedInFormats:
            mode.backend(
                install_deps=install_deps,
                verbose=verbose,
            )
        self._install_deps = install_deps
        self._verbose = verbose

    def compress(
        self,
        input_file: str | Path,
        output_file: str | Path,
        **kwargs: Any,
    ):
        """
        Execute the command to compress the input file.

        :param input_file: Input file path.
        :param output_file: Output file path.      
        :param kwargs: Arguments.

        :return: Subprocess.CompletedProcess object

        :raises RuntimeError: If backend encounters an error during execution.
        """
        # Execute the command
        output_file = Path(output_file)
        output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext = output_file.suffix[1:]

        backend = CompressBackend.SupportedOutFormats(out_ext).backend(
            install_deps=self._install_deps,
            verbose=self._verbose,
        )
        return backend.compress(
            input_file=input_file,
            output_file=output_file,
            **kwargs,
        )


__all__ = [
    "CompressBackend",
]
