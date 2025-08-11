# src\file_conversor\backend\writer_backend.py

import subprocess

from pathlib import Path
from typing import Iterable

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation
from file_conversor.backend.abstract_backend import AbstractBackend

LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WriterBackend(AbstractBackend):
    """
    A class that provides an interface for handling doc files using ``writer`` (libreoffice).
    """

    SUPPORTED_IN_FORMATS = {
        "doc": {},
        "docx": {},
        "odt": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "doc": {},
        "docx": {},
        "odt": {},
        "pdf": {},
        "html": {},
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

        self._libreoffice_bin = self.find_in_path("libreoffice")

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
        :raises RuntimeError: if LibreOffice fails.
        """
        self.check_file_exists(input_file)

        input_path = Path(input_file).resolve()
        output_path = Path(output_file).resolve()

        output_dir = output_path.parent
        output_format = output_path.suffix.lstrip(".").lower()

        command = [
            str(self._libreoffice_bin),
            "--headless",
            "--convert-to",
            str(output_format),
            "--outdir",
            str(output_dir),
            str(input_path)
        ]

        # Execute command
        logger.info("Executing LibreOffice ...")
        logger.debug(" ".join(command))
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        process.wait()
        if process.returncode != 0:
            raise RuntimeError(
                f"{_('LibreOffice conversion failed with error code')} '{process.returncode}': {process.stderr}"
            )
