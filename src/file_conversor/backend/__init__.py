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
from file_conversor.backend.office import *
from file_conversor.backend.pdf import *

# OTHER BACKENDS
from file_conversor.backend.batch_backend import *
from file_conversor.backend.git_backend import *
from file_conversor.backend.hash_backend import *
from file_conversor.backend.http_backend import *
from file_conversor.backend.text_backend import *
from file_conversor.backend.win_reg_backend import *
