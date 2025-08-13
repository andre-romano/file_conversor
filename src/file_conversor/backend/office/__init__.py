"""
Module for LibreOffice backend (calc, writer, etc)
"""

from file_conversor.backend.office.calc_backend import LibreofficeCalcBackend
from file_conversor.backend.office.excel_backend import ExcelBackend

from file_conversor.backend.office.impress_backend import LibreofficeImpressBackend
from file_conversor.backend.office.powerpoint_backend import PowerPointBackend

from file_conversor.backend.office.writer_backend import LibreofficeWriterBackend
from file_conversor.backend.office.word_backend import WordBackend

DOC_BACKEND = WordBackend if WordBackend().is_available() else LibreofficeWriterBackend
XLS_BACKEND = ExcelBackend if ExcelBackend().is_available() else LibreofficeCalcBackend
PPT_BACKEND = PowerPointBackend if PowerPointBackend().is_available() else LibreofficeImpressBackend
