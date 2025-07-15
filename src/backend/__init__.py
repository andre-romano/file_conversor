# src/backend/__init__.py

"""
Initialization module for the backend package.

This module imports all functionalities from backend wrappers,
making them available when importing the backend package.
"""

from backend.backend_abstract import BackendAbstract
from backend.ffmpeg_backend import FFmpegBackend
