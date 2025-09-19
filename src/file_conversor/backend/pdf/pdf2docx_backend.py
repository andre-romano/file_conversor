# src\file_conversor\backend\pdf2docx_backend.py

from pdf2docx import Converter

from pathlib import Path

from typing import Any, Callable

# user-provided imports
from file_conversor.config import Environment, Log, State
from file_conversor.config.locale import get_translation

from file_conversor.backend.abstract_backend import AbstractBackend

STATE = State.get_instance()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()


class PDF2DOCXBackend(AbstractBackend):

    SUPPORTED_IN_FORMATS = {
        "pdf": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "docx": {},
    }
    EXTERNAL_DEPENDENCIES = set([])

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

    def to_docx(self,
                output_file: str | Path,
                input_file: str | Path,
                password: str | None = None,
                ):
        """
        Convert input files into output file.

        :param output_file: Output file
        :param input_file: Input file. 

        :raises FileNotFoundError: if input file not found
        """
        input_file = Path(input_file).resolve()
        output_file = Path(output_file).resolve()

        self.check_file_exists(input_file)

        converter = Converter(
            pdf_file=str(input_file),
            password=password,  # pyright: ignore[reportArgumentType]
        )
        converter.convert(str(output_file))
        converter.close()
