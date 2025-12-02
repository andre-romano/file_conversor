# src\file_conversor\backend\office\word_backend.py

from pathlib import Path
from typing import Any, Callable

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation
from file_conversor.backend.office.abstract_msoffice_backend import AbstractMSOfficeBackend, Win32Com

LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WordBackend(AbstractMSOfficeBackend):
    """
    A class that provides an interface for handling doc files using ``word`` (comtypes).
    """

    SUPPORTED_IN_FORMATS = {
        "doc": {},
        "docx": {},
        "odt": {},
        "pdf": {},
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
            prog_id="Word.Application",
            install_deps=install_deps,
            verbose=verbose,
        )

    def convert(
        self,
        files: list[tuple[Path, Path]],
        file_processed_callback: Callable[[Path], Any] | None = None,
    ):
        with Win32Com(self.PROG_ID, visible=None) as word:
            for input_file, output_file in files:
                self.check_file_exists(input_file)

                input_path = input_file.resolve()

                output_path = output_file.resolve()
                output_path = output_path.with_suffix(output_path.suffix.lower())

                out_ext = output_path.suffix[1:]
                out_config = WordBackend.SUPPORTED_OUT_FORMATS[out_ext]

                doc = word.Documents.Open(str(input_path))
                doc.SaveAs(
                    str(output_path),
                    FileFormat=out_config['format'],
                )
                doc.Close()

                if file_processed_callback:
                    file_processed_callback(input_path)


__all__ = [
    "WordBackend",
]
