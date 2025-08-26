# src\file_conversor\cli\_info.py

from typing import Any

# user-provided modules
from file_conversor.config import get_translation
from file_conversor.system import CURR_PLATFORM, PLATFORM_WINDOWS

# CLI
from file_conversor.cli.audio_video import audio_video_cmd
from file_conversor.cli.config import config_cmd
from file_conversor.cli.doc import doc_cmd
from file_conversor.cli.hash import hash_cmd
from file_conversor.cli.image import image_cmd
from file_conversor.cli.pdf import pdf_cmd
from file_conversor.cli.pipeline import pipeline_cmd
from file_conversor.cli.ppt import ppt_cmd
from file_conversor.cli.text import text_cmd
from file_conversor.cli.win import win_cmd
from file_conversor.cli.xls import xls_cmd

_ = get_translation()

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
        "name": "doc",
        "help": f"{_('Document file manipulation')} {_('(requires MS Office / LibreOffice)')})",
        "rich_help_panel": OFFICE_PANEL,
    },
    {
        "typer_instance": xls_cmd,
        "name": "xls",
        "help": f"{_('Spreadsheet file manipulation')} {_('(requires MS Office / LibreOffice)')})",
        "rich_help_panel": OFFICE_PANEL,
    },
    {
        "typer_instance": ppt_cmd,
        "name": "ppt",
        "help": f"{_('Presentation file manipulation')} {_('(requires MS Office / LibreOffice)')})",
        "rich_help_panel": OFFICE_PANEL,
    },
])

################
# FILE PANEL #
################
COMMANDS_LIST.extend([
    {
        "typer_instance": audio_video_cmd,
        "name": "audio-video",
        "help": _("Audio / Video file manipulation (requires FFMpeg external library)"),
        "rich_help_panel": FILE_PANEL
    },
    {

        "typer_instance": image_cmd,
        "name": "image",
        "help": _("Image file manipulation"),
        "rich_help_panel": FILE_PANEL
    },
    {

        "typer_instance": pdf_cmd,
        "name": "pdf",
        "help": _("PDF file manipulation"),
        "rich_help_panel": FILE_PANEL
    },
    {
        "typer_instance": text_cmd,
        "name": "text",
        "help": _("Text file manipulation (json, xml, etc)"),
        "rich_help_panel": FILE_PANEL
    },
    {
        "typer_instance": hash_cmd,
        "name": "hash",
        "help": _("Hashing manipulation (check, gen, etc)"),
        "rich_help_panel": FILE_PANEL
    },
])


######################
# UTILS/CONFIG PANEL
######################
if CURR_PLATFORM == PLATFORM_WINDOWS:
    COMMANDS_LIST.append({
        "typer_instance": win_cmd,
        "name": "win",
        "help": _("Windows OS commands (for Windows ONLY)"),
        "rich_help_panel": UTILS_CONFIG_PANEL
    })

COMMANDS_LIST.extend([
    {
        "typer_instance": config_cmd,
        "name": "config",
        "help": _("Configure default options"),
        "rich_help_panel": UTILS_CONFIG_PANEL,
    },
    {
        "typer_instance": pipeline_cmd,
        "name": "pipeline",
        "help": f"""{_('Pipeline file processing (task automation)')}

                {_('The pipeline processsing by processing an input folder, passing those files to the next pipeline stage, and processing them inside that stage. This process continues (output of the current stage is the input of the next stage), until those files reach the end of the pipeline.')}



                {_('Example')}:

                - {_('Input folder')} => {_('Stage 1')} => {_('Stage 2')} => ... => {_('Output Folder')}
        """,
        "rich_help_panel": UTILS_CONFIG_PANEL,
    },
])
