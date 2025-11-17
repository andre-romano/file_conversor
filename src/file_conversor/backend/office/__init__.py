"""
Module for LibreOffice backend (calc, writer, etc)
"""

from pathlib import Path
from typing import List

from file_conversor.backend.office.calc_backend import LibreofficeCalcBackend
from file_conversor.backend.office.impress_backend import LibreofficeImpressBackend
from file_conversor.backend.office.writer_backend import LibreofficeWriterBackend

__all__ = [
    "LibreofficeCalcBackend",
    "LibreofficeWriterBackend",
    "LibreofficeImpressBackend",
]
