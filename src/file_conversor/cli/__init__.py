# src\file_conversor\cli\__init__.py

import sys
import typer

from enum import Enum
from pathlib import Path
from typing import Annotated, Any

# user-provided imports
from file_conversor.cli._utils import AbstractTyperGroup

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

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import AVAILABLE_LANGUAGES, get_system_locale, get_translation

from file_conversor.system import System

# Get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _overwrite_output_callback(value: bool):
    STATE.overwrite_output.enabled = value


def _no_log_callback(value: bool):
    STATE.logfile.enabled = not value


def _no_progress_callback(value: bool):
    STATE.progress.enabled = not value


def _quiet_callback(value: bool):
    if value:
        STATE.loglevel.level = Log.Level.ERROR


def _verbose_callback(value: bool):
    if value:
        STATE.loglevel.level = Log.Level.INFO


def _debug_callback(value: bool):
    if value:
        STATE.loglevel.level = Log.Level.DEBUG


def _version_callback(value: bool):
    if not value:
        return
    logger.info(f"File Conversor {Environment.get_app_version()}")
    logger.info(f"Python {Environment.get_python_version()} ({sys.executable})")
    logger.info(f"System: {System.Platform.get()}")
    raise typer.Exit()


def _self_test_callback(value: bool):
    if not value:
        return
    try:
        # show version info
        _version_callback(True)
    except typer.Exit:
        pass

    from file_conversor.config.self_tests import SelfTests
    SelfTests().run_self_tests()

    raise typer.Exit()


class AppTyperGroup(AbstractTyperGroup):
    # PANELS
    class Panels(Enum):
        OFFICE = _("Office files")
        FILE = _("Other files")
        UTILS_CONFIG = _("Utils and Config")

    # COMMANDS
    class Commands(Enum):
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

    # main callback to pass common options
    @classmethod
    def _main_callback(
        cls,
        no_log: Annotated[bool, typer.Option(
            "--no-log", "-nl",
            help=_("Disable file logs"),
            callback=_no_log_callback,
            is_flag=True,
        )] = False,
        no_progress: Annotated[bool, typer.Option(
            "--no-progress", "-np",
            help=f"{_('Disable progress bars')}",
            callback=_no_progress_callback,
            is_flag=True,
        )] = False,
        quiet: Annotated[bool, typer.Option(
            "--quiet", "-q",
            help=f"{_('Enable quiet mode (only display errors and progress bars)')}",
            callback=_quiet_callback,
            is_flag=True,
        )] = False,
        verbose: Annotated[bool, typer.Option(
            "--verbose", "-v",
            help=_("Enable verbose mode"),
            callback=_verbose_callback,
            is_flag=True,
        )] = False,
        debug: Annotated[bool, typer.Option(
            "--debug", "-d",
            help=_("Enable debug mode"),
            callback=_debug_callback,
            is_flag=True,
        )] = False,
        overwrite_output: Annotated[bool, typer.Option(
            "--overwrite-output", "-oo",
            help=f"{_('Overwrite output files')}. Defaults to False (do not overwrite).",
            callback=_overwrite_output_callback,
            is_flag=True,
        )] = False,
        version: Annotated[bool, typer.Option(
            "--version", "-V",
            help=_("Display version"),
            callback=_version_callback,
            is_flag=True,
        )] = False,
        self_test: Annotated[bool, typer.Option(
            "--self-test", "-st",
            help=_("Run self tests"),
            callback=_self_test_callback,
            is_flag=True,
        )] = False,
    ):
        try:
            # show version info
            _version_callback(True)
        except typer.Exit:
            pass
        logger.debug(f"Command: {sys.argv}")
        # Environment.get_executable()
        logger.debug(f"Working directory: {Path().resolve()}")
        logger.debug(f"Resources folder: {Environment.get_resources_folder()}")
        logger.debug(f"Data folder: {Environment.get_data_folder()}")
        logger.debug(f"Available languages: {sorted(AVAILABLE_LANGUAGES)} ({len(AVAILABLE_LANGUAGES)} entries)")
        logger.debug(f"Language (config / sys): ({CONFIG.language} / {get_system_locale()})")

    def __init__(self) -> None:
        super().__init__(
            rich_markup_mode=AbstractTyperGroup.MarkupMode.MARKDOWN,
            context_settings={
                "help_option_names": ["-h", "--help"],
            },
            callback=AbstractTyperGroup.CallbackDataModel(
                function=self._main_callback,
                help=f"""
    # File Conversor - CLI
""",
                epilog=f"""
    {_('For more information, visit')} [http://www.github.com/andre-romano/file_conversor](http://www.github.com/andre-romano/file_conversor)
"""
            ),
        )

        # add subcommands
        self.add(
            # OFFICE
            DocTyperGroup(self.Commands.DOC.value, rich_help_panel=self.Panels.OFFICE.value),
            XlsTyperGroup(self.Commands.XLS.value, rich_help_panel=self.Panels.OFFICE.value),
            PptTyperGroup(self.Commands.PPT.value, rich_help_panel=self.Panels.OFFICE.value),

            # FILE
            AudioTyperGroup(self.Commands.AUDIO.value, rich_help_panel=self.Panels.FILE.value),
            VideoTyperGroup(self.Commands.VIDEO.value, rich_help_panel=self.Panels.FILE.value),
            ImageTyperGroup(self.Commands.IMAGE.value, rich_help_panel=self.Panels.FILE.value),
            PdfTyperGroup(self.Commands.PDF.value, rich_help_panel=self.Panels.FILE.value),
            EbookTyperGroup(self.Commands.EBOOK.value, rich_help_panel=self.Panels.FILE.value),
            TextTyperGroup(self.Commands.TEXT.value, rich_help_panel=self.Panels.FILE.value),
            HashTyperGroup(self.Commands.HASH.value, rich_help_panel=self.Panels.FILE.value),

            # UTILS and CONFIG
            WinTyperGroup(self.Commands.WIN.value, rich_help_panel=self.Panels.UTILS_CONFIG.value, hidden=System.Platform.get() != System.Platform.WINDOWS),
            ConfigTyperGroup(self.Commands.CONFIG.value, rich_help_panel=self.Panels.UTILS_CONFIG.value),
            PipelineTyperGroup(self.Commands.PIPELINE.value, rich_help_panel=self.Panels.UTILS_CONFIG.value),
        )

    def run(self):
        self._typer_cmd(prog_name=Environment.get_app_name())


__all__ = [
    "AppTyperGroup",
]
