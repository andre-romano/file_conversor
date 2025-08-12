"""
Module for LibreOffice backend (calc, writer, etc)
"""

from file_conversor.system import CURR_PLATFORM, PLATFORM_WINDOWS

from file_conversor.backend.office.calc_backend import LibreofficeCalcBackend
from file_conversor.backend.office.excel_backend import ExcelBackend

from file_conversor.backend.office.impress_backend import LibreofficeImpressBackend
from file_conversor.backend.office.powerpoint_backend import PowerPointBackend

from file_conversor.backend.office.writer_backend import LibreofficeWriterBackend
from file_conversor.backend.office.word_backend import WordBackend

if CURR_PLATFORM == PLATFORM_WINDOWS:
    DOC_BACKEND = WordBackend
    XLS_BACKEND = ExcelBackend
    PPT_BACKEND = PowerPointBackend
else:
    DOC_BACKEND = LibreofficeWriterBackend
    XLS_BACKEND = LibreofficeCalcBackend
    PPT_BACKEND = LibreofficeImpressBackend
