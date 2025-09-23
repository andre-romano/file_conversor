# src\file_conversor\backend\__init__.py

"""
Initialization module for the backend package.

This module imports all functionalities from backend wrappers,
making them available when importing the backend package.
"""

# SUBMODULES
from file_conversor.backend.audio_video import *
from file_conversor.backend.ebook import *
from file_conversor.backend.image import *
from file_conversor.backend.office import DOC_BACKEND, XLS_BACKEND, PPT_BACKEND
from file_conversor.backend.pdf import *

# OTHER BACKENDS
from file_conversor.backend.batch_backend import BatchBackend
from file_conversor.backend.git_backend import GitBackend
from file_conversor.backend.hash_backend import HashBackend
from file_conversor.backend.http_backend import HttpBackend
from file_conversor.backend.text_backend import TextBackend
from file_conversor.backend.win_reg_backend import WinRegBackend
