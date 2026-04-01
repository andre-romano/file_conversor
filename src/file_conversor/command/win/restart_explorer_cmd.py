
# src\file_conversor\command\win\restart_explorer_cmd.py

from enum import StrEnum
from typing import override

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.system import System, WindowsSystem


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


WinRestartExplorerExternalDependencies: set[str] = set()


class WinRestartExplorerInFormats(StrEnum):
    """ empty enum since this command does not process files, but is just a system command to restart explorer.exe """


class WinRestartExplorerOutFormats(StrEnum):
    """ empty enum since this command does not process files, but is just a system command to restart explorer.exe """


class WinRestartExplorerCommand(AbstractCommand[WinRestartExplorerInFormats, WinRestartExplorerOutFormats]):
    @classmethod
    @override
    def _external_dependencies(cls):
        return WinRestartExplorerExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return WinRestartExplorerInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return WinRestartExplorerOutFormats

    @override
    def execute(self):
        if not isinstance(System, WindowsSystem):
            raise RuntimeError(_("Restart Explorer command can only be executed on Windows systems"))
        logger.info(f"{_('Restarting explorer.exe')} ...")
        System.restart_explorer()
        self.progress_callback(100.0)


__all__ = [
    "WinRestartExplorerExternalDependencies",
    "WinRestartExplorerInFormats",
    "WinRestartExplorerOutFormats",
    "WinRestartExplorerCommand",
]
