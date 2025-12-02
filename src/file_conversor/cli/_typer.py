# src\file_conversor\cli\_info.py

import sys
import typer

from typing import Any

# user-provided modules
from file_conversor.config import get_translation
from file_conversor.system import is_windows

# CLI
from file_conversor.cli.audio import audio_cmd
from file_conversor.cli.video import video_cmd
from file_conversor.cli.config import config_cmd
from file_conversor.cli.doc import doc_cmd
from file_conversor.cli.ebook import ebook_cmd
from file_conversor.cli.gui import gui_cmd
from file_conversor.cli.hash import hash_cmd
from file_conversor.cli.image import image_cmd
from file_conversor.cli.pdf import pdf_cmd
from file_conversor.cli.pipeline import pipeline_cmd
from file_conversor.cli.ppt import ppt_cmd
from file_conversor.cli.text import text_cmd
from file_conversor.cli.win import win_cmd
from file_conversor.cli.xls import xls_cmd

_ = get_translation()

PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

# PANELS
OFFICE_PANEL = _("Office files")
FILE_PANEL = _("Other files")
UTILS_CONFIG_PANEL = _("Utils and Config")

# COMMANDS
COMMANDS_LIST: list[dict[str, Any]] = []

################
# OFFICE PANEL #
################
COMMANDS_LIST.extend([
    {
        "typer_instance": doc_cmd,
        "rich_help_panel": OFFICE_PANEL,
    },
    {
        "typer_instance": xls_cmd,
        "rich_help_panel": OFFICE_PANEL,
    },
    {
        "typer_instance": ppt_cmd,
        "rich_help_panel": OFFICE_PANEL,
    },
])

################
# FILE PANEL #
################
COMMANDS_LIST.extend([
    {
        "typer_instance": audio_cmd,
        "rich_help_panel": FILE_PANEL
    },
    {
        "typer_instance": video_cmd,
        "rich_help_panel": FILE_PANEL
    },
    {

        "typer_instance": image_cmd,
        "rich_help_panel": FILE_PANEL
    },
    {

        "typer_instance": pdf_cmd,
        "rich_help_panel": FILE_PANEL
    },
    {

        "typer_instance": ebook_cmd,
        "rich_help_panel": FILE_PANEL
    },
    {
        "typer_instance": text_cmd,
        "rich_help_panel": FILE_PANEL
    },
    {
        "typer_instance": hash_cmd,
        "rich_help_panel": FILE_PANEL
    },
])


######################
# UTILS/CONFIG PANEL
######################
if is_windows():
    COMMANDS_LIST.append({
        "typer_instance": win_cmd,
        "rich_help_panel": UTILS_CONFIG_PANEL
    })

COMMANDS_LIST.extend([
    {
        "typer_instance": config_cmd,
        "rich_help_panel": UTILS_CONFIG_PANEL,
    },
    {
        "typer_instance": pipeline_cmd,
        "rich_help_panel": UTILS_CONFIG_PANEL,
    },
    {
        "typer_instance": gui_cmd,
        "rich_help_panel": UTILS_CONFIG_PANEL,
    },
])

__all__ = [
    "PYTHON_VERSION",
    "COMMANDS_LIST",
]
