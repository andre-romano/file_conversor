# src\file_conversor\backend\office\powerpoint_backend.py

from enum import Enum
from pathlib import Path
from typing import override

from file_conversor.backend.office.abstract_msoffice_backend import (
    AbstractMSOfficeBackend,
    Win32Com,
)

# user-provided imports
from file_conversor.config import Log, get_translation


LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PowerPointBackend(AbstractMSOfficeBackend):
    """
    A class that provides an interface for handling doc files using ``powerpoint`` (comtypes).
    """

    class SupportedInFormats(Enum):
        PPT = "ppt"
        PPTX = "pptx"
        ODP = "odp"

    class SupportedOutFormats(Enum):
        PPT = "ppt"
        PPTX = "pptx"
        ODP = "odp"
        PDF = "pdf"

        @property
        def format(self) -> int:
            """ 
            Get VBA code for the format, check API docs below:

            https://learn.microsoft.com/en-us/office/vba/api/powerpoint.ppsaveasfiletype

            :return: VBA code for the format
            """
            match self:
                case PowerPointBackend.SupportedOutFormats.PPT:
                    return 1
                case PowerPointBackend.SupportedOutFormats.PPTX:
                    return 24
                case PowerPointBackend.SupportedOutFormats.ODP:
                    return 35
                case PowerPointBackend.SupportedOutFormats.PDF:
                    return 32

    EXTERNAL_DEPENDENCIES: set[str] = set()

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

    @override
    def convert(
        self,
        input_path: Path,
        output_path: Path,
    ):
        with Win32Com(self.PROG_ID, visible=None) as powerpoint:
            output_path = output_path.with_suffix(output_path.suffix.lower())

            out_ext = output_path.suffix[1:]
            file_format_vba_code = PowerPointBackend.SupportedOutFormats(out_ext.upper()).format

            # powerpoint.Visible -> True  # needed for powerpoint
            presentation = powerpoint.Presentations.Open(str(input_path), WithWindow=False)
            presentation.SaveAs(
                str(output_path),
                FileFormat=file_format_vba_code,
            )
            presentation.Close()


__all__ = [
    "PowerPointBackend",
]
