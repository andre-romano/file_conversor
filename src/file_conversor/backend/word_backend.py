# src\file_conversor\backend\word_backend.py

from pathlib import Path
from typing import Iterable

# user-provided imports
from file_conversor.system import CURR_PLATFORM, PLATFORM_WINDOWS
from file_conversor.config import Log
from file_conversor.config.locale import get_translation
from file_conversor.backend.abstract_backend import AbstractBackend

# conditional import
if CURR_PLATFORM == PLATFORM_WINDOWS:
    from win32com import client
else:
    client = None

LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WordBackend(AbstractBackend):
    """
    A class that provides an interface for handling doc files using ``word`` (comtypes).
    """

    SUPPORTED_IN_FORMATS = {
        "doc": {},
        "docx": {},
        "odt": {},
    }
    SUPPORTED_OUT_FORMATS = {
        # format = wdFormat VBA code
        # https://learn.microsoft.com/en-us/office/vba/api/word.wdsaveformat
        "doc": {'format': 0},
        "docx": {'format': 16},
        "odt": {'format': 23},
        "pdf": {'format': 17},
        "html": {'format': 8},
    }

    def __init__(
        self,
        verbose: bool = False,
    ):
        """
        Initialize the backend

        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__()
        self._verbose = verbose

    def convert(
        self,
        output_file: str,
        input_file: str,
    ):
        """
        Convert input file into an output file.

        :param output_file: Output file.
        :param input_file: Input file.        

        :raises FileNotFoundError: if input file not found.
        :raises RuntimeError: if os != Windows.
        """
        if not client:
            raise RuntimeError("This backend supports only Windows OS")
        input_path = Path(input_file).resolve()
        output_path = Path(output_file).resolve()

        self.check_file_exists(str(input_path))

        out_config = WordBackend.SUPPORTED_OUT_FORMATS[output_path.suffix[1:]]

        word = client.Dispatch("Word.Application")
        doc = word.Documents.Open(str(input_path))
        doc.SaveAs(str(output_path),
                   FileFormat=out_config['format'],
                   )
        doc.Close()
        try:
            word.Quit()
        except:
            logger.warning(f"{_('Failed to close Word properly')}.")
