# src\file_conversor\backend\office\excel_backend.py

from enum import Enum
from pathlib import Path
from typing import override

from file_conversor.backend.office.abstract_msoffice_backend import (
    AbstractMSOfficeBackend,
    Win32Com,
)
from file_conversor.config import Log, get_translation


LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ExcelBackend(AbstractMSOfficeBackend):
    """
    A class that provides an interface for handling doc files using ``excel`` (comtypes).
    """

    class SupportedInFormats(Enum):
        XLS = "xls"
        XLSX = "xlsx"
        ODS = "ods"

    class SupportedOutFormats(Enum):
        XLS = "xls"
        XLSX = "xlsx"
        ODS = "ods"
        CSV = "csv"
        PDF = "pdf"
        HTML = "html"

        @property
        def format(self) -> int:
            """ 
            Get xlFormat VBA code, check API docs below:

            https://learn.microsoft.com/en-us/office/vba/api/excel.xlfileformat

            :return: VBA code for the format
            """
            match self:
                case ExcelBackend.SupportedOutFormats.XLS:
                    return 56
                case ExcelBackend.SupportedOutFormats.XLSX:
                    return 51
                case ExcelBackend.SupportedOutFormats.ODS:
                    return 60
                case ExcelBackend.SupportedOutFormats.CSV:
                    return 6
                case ExcelBackend.SupportedOutFormats.PDF:
                    return 57
                case ExcelBackend.SupportedOutFormats.HTML:
                    return 44

    EXTERNAL_DEPENDENCIES: set[str] = set()

    def __init__(
        self,
        install_deps: bool | None = None,
        verbose: bool = False,
    ):
        """
        Initialize the backend

        :param install_deps: Reserved for future use. 
        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__(
            prog_id="Excel.Application",
            install_deps=install_deps,
            verbose=verbose,
        )

    @override
    def convert(
        self,
        input_path: Path,
        output_path: Path,
    ):
        with Win32Com(self.PROG_ID, visible=False) as excel:
            output_path = output_path.with_suffix(output_path.suffix.lower())

            out_ext = output_path.suffix[1:]
            format_vba_code = ExcelBackend.SupportedOutFormats(out_ext.upper()).format

            workbook = excel.Workbooks.Open(str(input_path))
            if output_path.suffix.lower() == ".pdf":
                workbook.ExportAsFixedFormat(
                    Filename=str(output_path),
                    Type=0,  # = pdf
                    Quality=0,
                    IncludeDocProperties=True,
                    IgnorePrintAreas=False,
                    OpenAfterPublish=False,
                )
            else:
                workbook.SaveAs(
                    str(output_path),
                    FileFormat=format_vba_code,
                )
            workbook.Close(SaveChanges=False)


__all__ = [
    "ExcelBackend",
]
