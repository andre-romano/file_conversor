# src\file_conversor\backend\docx2pdf_backend.py

"""
This module provides functionalities for handling document files using ``docx2pdf``.
"""

import shutil
import subprocess

from docx2pdf import convert

# user-provided imports
from file_conversor.config.log import Log
from file_conversor.config.locale import get_translation

from file_conversor.backend.abstract_backend import AbstractBackend

LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class Docx2PDFBackend(AbstractBackend):
    """
    A class that provides an interface for handling document files using ``docx2pdf``.
    """

    SUPPORTED_IN_FORMATS = {
        "docx": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "pdf": {},
    }

    def __init__(self):
        """
        Initialize the ``docx2pdf`` backend
        """
        super().__init__()

    def to_pdf(
        self,
        output_file: str,
        input_file: str,
    ):
        """
        Convert input file into an output PDF file.

        :param output_file: Output image file.
        :param input_file: Input image file.        

        :raises FileNotFoundError: if input file not found.
        """
        try:
            self.check_file_exists(input_file)
            convert(input_path=input_file, output_path=output_file, keep_active=True)
        except AttributeError as e:
            if ("Word.Application.Quit" in str(e)):
                logger.error(f"{_('Failed to quit Word properly. Consider restarting Word manually.')}")
                return
            raise
