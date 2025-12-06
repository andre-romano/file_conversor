# src\file_conversor\backend\office\powerpoint_backend.py

from pathlib import Path
from typing import Any, Callable

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation
from file_conversor.backend.office.abstract_msoffice_backend import AbstractMSOfficeBackend, Win32Com

LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PowerPointBackend(AbstractMSOfficeBackend):
    """
    A class that provides an interface for handling doc files using ``powerpoint`` (comtypes).
    """

    SUPPORTED_IN_FORMATS = {
        "ppt": {},
        "pptx": {},
        "odp": {},
    }
    SUPPORTED_OUT_FORMATS = {
        # format = wdFormat VBA code
        # https://learn.microsoft.com/en-us/office/vba/api/powerpoint.ppsaveasfiletype
        "ppt": {'format': 1},
        "pptx": {'format': 24},
        "odp": {'format': 35},
        "pdf": {'format': 32},
    }
    EXTERNAL_DEPENDENCIES = set()

    def __init__(
        self,
        install_deps: bool | None = None,
        verbose: bool = False,
    ):
        """
        Initialize the backend

        :param install_deps: Reserved for future use. Defaults to None.
        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__(
            prog_id="PowerPoint.Application",
            install_deps=install_deps,
            verbose=verbose,
        )

    def convert(
        self,
        files: list[tuple[Path, Path]],
        file_processed_callback: Callable[[Path], Any] | None = None,
    ):
        with Win32Com(self.PROG_ID, visible=None) as powerpoint:
            for input_file, output_file in files:
                input_path = input_file.resolve()

                output_path = output_file.resolve()
                output_path = output_path.with_suffix(output_path.suffix.lower())

                self.check_file_exists(str(input_path))

                out_ext = output_path.suffix[1:]
                out_config = PowerPointBackend.SUPPORTED_OUT_FORMATS[out_ext]

                # powerpoint.Visible -> True  # needed for powerpoint
                presentation = powerpoint.Presentations.Open(str(input_path), WithWindow=False)
                presentation.SaveAs(
                    str(output_path),
                    FileFormat=out_config['format'],
                )
                presentation.Close()

                if file_processed_callback:
                    file_processed_callback(input_path)


__all__ = [
    "PowerPointBackend",
]
