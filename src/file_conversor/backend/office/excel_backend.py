# src\file_conversor\backend\office\excel_backend.py

from pathlib import Path

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation
from file_conversor.backend.office.abstract_msoffice_backend import AbstractMSOfficeBackend, Win32Com

LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ExcelBackend(AbstractMSOfficeBackend):
    """
    A class that provides an interface for handling doc files using ``excel`` (comtypes).
    """

    SUPPORTED_IN_FORMATS = {
        "xls": {},
        "xlsx": {},
        "ods": {},
    }
    SUPPORTED_OUT_FORMATS = {
        # format = xlFormat VBA code
        # https://learn.microsoft.com/en-us/office/vba/api/excel.xlfileformat
        "xls": {'format': 56},
        "xlsx": {'format': 51},
        "ods": {'format': 60},
        "csv": {'format': 6},
        "pdf": {'format': 57},
        "html": {'format': 44},
    }
    EXTERNAL_DEPENDENCIES = set()

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

    def convert(
        self,
        output_file: str | Path,
        input_file: str | Path,
    ):
        """
        Convert input file into an output file.

        :param output_file: Output file.
        :param input_file: Input file.        

        :raises FileNotFoundError: if input file not found.
        :raises RuntimeError: if os != Windows.
        """
        input_path = Path(input_file).resolve()
        output_path = Path(output_file).resolve()

        self.check_file_exists(str(input_path))

        out_config = ExcelBackend.SUPPORTED_OUT_FORMATS[output_path.suffix[1:]]

        with Win32Com(self.PROG_ID, visible=False) as excel:
            workbook = excel.Workbooks.Open(str(input_path))
            if output_path.suffix.lower() == ".pdf":
                workbook.ExportAsFixedFormat(
                    Filename=str(output_path),
                    Type=0,  # 0 = pdf
                    Quality=0,
                    IncludeDocProperties=True,
                    IgnorePrintAreas=False,
                    OpenAfterPublish=False,
                )
            else:
                workbook.SaveAs(
                    str(output_path),
                    FileFormat=out_config['format'],
                )
            workbook.Close(SaveChanges=False)
