# src\file_conversor\backend\office\word_backend.py

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


class WordBackend(AbstractMSOfficeBackend):
    """
    A class that provides an interface for handling doc files using ``word`` (comtypes).
    """

    class SupportedInFormats(Enum):
        DOC = "doc"
        DOCX = "docx"
        ODT = "odt"
        PDF = "pdf"

    class SupportedOutFormats(Enum):
        DOC = "doc"
        DOCX = "docx"
        ODT = "odt"
        PDF = "pdf"
        HTML = "html"

        @property
        def format(self) -> int:
            """ 
            Get wdFormat VBA code, check API docs below:

            https://learn.microsoft.com/en-us/office/vba/api/word.wdsaveformat

            :return: VBA code for the format
            """
            match self:
                case WordBackend.SupportedOutFormats.DOC:
                    return 0
                case WordBackend.SupportedOutFormats.DOCX:
                    return 16
                case WordBackend.SupportedOutFormats.ODT:
                    return 23
                case WordBackend.SupportedOutFormats.PDF:
                    return 17
                case WordBackend.SupportedOutFormats.HTML:
                    return 8

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
            prog_id="Word.Application",
            install_deps=install_deps,
            verbose=verbose,
        )

    @override
    def convert(
        self,
        input_path: Path,
        output_path: Path,
    ):
        with Win32Com(self.PROG_ID, visible=None) as word:
            output_path = output_path.with_suffix(output_path.suffix.lower())

            out_ext = output_path.suffix[1:]
            format_vba_code = WordBackend.SupportedOutFormats(out_ext.upper()).format

            doc = word.Documents.Open(str(input_path))
            doc.SaveAs(
                str(output_path),
                FileFormat=format_vba_code,
            )
            doc.Close()


__all__ = [
    "WordBackend",
]
