# src\file_conversor\backend\compress_backend.py

from pathlib import Path
from typing import Any

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation

from file_conversor.backend.abstract_backend import AbstractBackend

from file_conversor.backend.image._gifsicle_backend import _GifSicleBackend
from file_conversor.backend.image._mozjpeg_backend import _MozJPEGBackend
from file_conversor.backend.image._oxipng_backend import _OxiPNGBackend

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class CompressBackend(AbstractBackend):
    """
    Provides an interface for handling files using mozjpeg.
    """

    SUPPORTED_IN_FORMATS: dict[str, dict[str, type]] = {
        "gif": {
            "cls": _GifSicleBackend
        },
        "jpg": {
            "cls": _MozJPEGBackend
        },
        "jpeg": {
            "cls": _MozJPEGBackend
        },
        "png": {
            "cls": _OxiPNGBackend
        },
    }
    SUPPORTED_OUT_FORMATS = SUPPORTED_IN_FORMATS
    EXTERNAL_DEPENDENCIES = {
        *_GifSicleBackend.EXTERNAL_DEPENDENCIES,
        *_MozJPEGBackend.EXTERNAL_DEPENDENCIES,
        *_OxiPNGBackend.EXTERNAL_DEPENDENCIES,
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
        for opts in CompressBackend.SUPPORTED_IN_FORMATS.values():
            cls = opts["cls"]
            cls(
                install_deps=install_deps,
                verbose=verbose,
            )
        self._install_deps = install_deps
        self._verbose = verbose

    def compress(
        self,
            input_file: str | Path,
            output_file: str | Path,
            **kwargs,
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

        out_opts = CompressBackend.SUPPORTED_OUT_FORMATS[out_ext]
        BACKEND_CLASS = out_opts["cls"]

        backend = BACKEND_CLASS(
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
