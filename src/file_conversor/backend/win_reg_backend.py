# src\file_conversor\backend\win_reg_backend.py

"""
This module provides functionalities for handling Windows Registry using ``reg`` backend.
"""

from enum import Enum
from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.abstract_backend import AbstractBackend

# user-provided imports
from file_conversor.config import Environment, Log
from file_conversor.system.win import WinRegFile


LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class WinRegBackend(AbstractBackend):
    """
    A class that provides an interface for handling .REG files using ``reg``.
    """

    class SupportedInFormats(Enum):
        REG = "reg"

    class SupportedOutFormats(Enum):
        REG = "reg"

    EXTERNAL_DEPENDENCIES: set[str] = set()

    def __init__(self, verbose: bool = False):
        """
        Initialize the ``reg`` backend

        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__()
        self._verbose = verbose

        self._reg_bin = self.find_in_path("reg")

    def import_file(
        self,
        input_file_or_winreg: Path | WinRegFile,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        """
        Import registry info from input .REG file.

        :param input_file_or_winreg: Input REG file, or WinRegFile.        
        :param progress_callback: Callback function to report progress, with a float parameter from 0.0 to 100.0. Defaults to a no-op lambda.

        :raises subprocess.CalledProcessError: if reg cannot import registry file
        """
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = (Path(temp_dir) / ".out.reg").resolve().__str__()

            winregfile: WinRegFile
            if isinstance(input_file_or_winreg, WinRegFile):
                winregfile = input_file_or_winreg
            else:
                winregfile = WinRegFile(input_file_or_winreg)
            winregfile.dump(temp_file)

            # build command
            Environment.run(
                f"{self._reg_bin}", "import", f"{temp_file}",
            )
            progress_callback(100.0)

    def delete_keys(
        self,
        input_file_or_winreg: Path | WinRegFile,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        """
        Loads registry keys from input .REG file, and deletes them from windows registry.

        :param input_file_or_winreg: Input .REG file.     
        :param progress_callback: Callback function to report progress, with a float parameter from 0.0 to 100.0. Defaults to a no-op lambda.   

        :raises subprocess.CalledProcessError: if reg cannot delete registry keys
        """
        import subprocess

        winregfile: WinRegFile
        if isinstance(input_file_or_winreg, WinRegFile):
            winregfile = input_file_or_winreg
        else:
            winregfile = WinRegFile(input_file_or_winreg)

        logger.info(f"Deleting reg keys ...")
        for _, key in winregfile.items():
            # Execute command
            try:
                Environment.run(
                    f"{self._reg_bin}", "query", f"{key.path}",
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except subprocess.CalledProcessError:
                # logger.debug(f"SKIP - key '{key.path}' not found ...")
                continue

            Environment.run(
                f"{self._reg_bin}", "delete", f"{key.path}", "/f",
            )

            logger.debug(f"'{key.path}' deleted")
            progress_callback(100.0 / len(winregfile))


__all__ = [
    "WinRegBackend",
]
