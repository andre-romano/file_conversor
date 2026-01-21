# src\file_conversor\cli\_info.py

import sys
import typer

from dataclasses import dataclass
from typing import Any, Iterable
from enum import Enum

# user-provided modules

# CLI
from file_conversor.cli.audio import AudioTyperGroup
from file_conversor.cli.config import ConfigTyperGroup
from file_conversor.cli.doc import DocTyperGroup
from file_conversor.cli.ebook import EbookTyperGroup
from file_conversor.cli.hash import HashTyperGroup
from file_conversor.cli.video import VideoTyperGroup
from file_conversor.cli.image import ImageTyperGroup
from file_conversor.cli.pdf import PdfTyperGroup
from file_conversor.cli.pipeline import PipelineTyperGroup
from file_conversor.cli.ppt import PptTyperGroup
from file_conversor.cli.text import TextTyperGroup
from file_conversor.cli.win import WinTyperGroup
from file_conversor.cli.xls import XlsTyperGroup

# core modules
from file_conversor.config import get_translation
from file_conversor.system import is_windows

_ = get_translation()

PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


# PANELS
class AppPanels(Enum):
    OFFICE = _("Office files")
    FILE = _("Other files")
    UTILS_CONFIG = _("Utils and Config")


# COMMANDS
class AppCommands(Enum):
    AUDIO = "audio"
    CONFIG = "config"
    DOC = "doc"
    EBOOK = "ebook"
    HASH = "hash"
    IMAGE = "image"
    PDF = "pdf"
    PIPELINE = "pipeline"
    PPT = "ppt"
    TEXT = "text"
    VIDEO = "video"
    WIN = "win"
    XLS = "xls"


def _get_commands_office() -> Iterable[typer.Typer]:
    return (
        DocTyperGroup(AppCommands.DOC.value, rich_help_panel=AppPanels.OFFICE.value).get_typer(),
        XlsTyperGroup(AppCommands.XLS.value, rich_help_panel=AppPanels.OFFICE.value).get_typer(),
        PptTyperGroup(AppCommands.PPT.value, rich_help_panel=AppPanels.OFFICE.value).get_typer(),
    )


def _get_commands_file() -> Iterable[typer.Typer]:
    return (
        AudioTyperGroup(AppCommands.AUDIO.value, rich_help_panel=AppPanels.FILE.value).get_typer(),
        VideoTyperGroup(AppCommands.VIDEO.value, rich_help_panel=AppPanels.FILE.value).get_typer(),
        ImageTyperGroup(AppCommands.IMAGE.value, rich_help_panel=AppPanels.FILE.value).get_typer(),
        PdfTyperGroup(AppCommands.PDF.value, rich_help_panel=AppPanels.FILE.value).get_typer(),
        EbookTyperGroup(AppCommands.EBOOK.value, rich_help_panel=AppPanels.FILE.value).get_typer(),
        TextTyperGroup(AppCommands.TEXT.value, rich_help_panel=AppPanels.FILE.value).get_typer(),
        HashTyperGroup(AppCommands.HASH.value, rich_help_panel=AppPanels.FILE.value).get_typer(),
    )


def _get_commands_utils_config() -> Iterable[typer.Typer]:
    return (
        *([] if not is_windows() else [
            WinTyperGroup(AppCommands.WIN.value, rich_help_panel=AppPanels.UTILS_CONFIG.value).get_typer()
        ]),
        ConfigTyperGroup(AppCommands.CONFIG.value, rich_help_panel=AppPanels.UTILS_CONFIG.value).get_typer(),
        PipelineTyperGroup(AppCommands.PIPELINE.value, rich_help_panel=AppPanels.UTILS_CONFIG.value).get_typer(),
    )


def get_commands() -> Iterable[typer.Typer]:
    # COMMANDS
    return (
        *_get_commands_office(),
        *_get_commands_file(),
        *_get_commands_utils_config(),
    )


__all__ = [
    "PYTHON_VERSION",
    "AppPanels",
    "AppCommands",
    "get_commands",
]
