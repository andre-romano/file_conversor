# src\file_conversor\backend\__init__.py

"""
Initialization module for the backend package.

This module imports all functionalities from backend wrappers,
making them available when importing the backend package.
"""

# SUBMODULES
from file_conversor.backend.office import DOC_BACKEND, XLS_BACKEND, PPT_BACKEND
from file_conversor.backend.pdf import *
from file_conversor.backend.image import *

# OTHER BACKENDS
from file_conversor.backend.batch_backend import BatchBackend
from file_conversor.backend.ffmpeg_backend import FFmpegBackend
from file_conversor.backend.hash_backend import HashBackend
from file_conversor.backend.text_backend import TextBackend
from file_conversor.backend.win_reg_backend import WinRegBackend
