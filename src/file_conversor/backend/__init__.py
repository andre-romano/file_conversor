# src\file_conversor\backend\__init__.py

"""
Initialization module for the backend package.

This module imports all functionalities from backend wrappers,
making them available when importing the backend package.
"""

# LIBREOFFICE / MSOFFICE
from file_conversor.backend.office import DOC_BACKEND, XLS_BACKEND, PPT_BACKEND

# OTHER BACKENDS
from file_conversor.backend.batch_backend import BatchBackend
from file_conversor.backend.ffmpeg_backend import FFmpegBackend
from file_conversor.backend.ghostscript_backend import GhostscriptBackend
from file_conversor.backend.img2pdf_backend import Img2PDFBackend
from file_conversor.backend.pillow_backend import PillowBackend
from file_conversor.backend.pymupdf_backend import PyMuPDFBackend
from file_conversor.backend.pymusvg_backend import PyMuSVGBackend
from file_conversor.backend.pypdf_backend import PyPDFBackend
from file_conversor.backend.qpdf_backend import QPDFBackend
from file_conversor.backend.win_reg_backend import WinRegBackend
