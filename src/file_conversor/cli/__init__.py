
# src\file_conversor\cli\__init__.py

"""
This module initializes the CLI commands package.
"""

# office
from file_conversor.cli.office import doc_cmd, xls_cmd, ppt_cmd

# other commands
from file_conversor.cli.audio_video_cmd import audio_video_cmd
from file_conversor.cli.batch_cmd import batch_cmd
from file_conversor.cli.config_cmd import config_cmd
from file_conversor.cli.image_cmd import image_cmd
from file_conversor.cli.pdf_cmd import pdf_cmd
from file_conversor.cli.svg_cmd import svg_cmd
from file_conversor.cli.win_cmd import win_cmd
