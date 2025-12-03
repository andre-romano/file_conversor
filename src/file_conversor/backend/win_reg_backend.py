# src\file_conversor\backend\win_reg_backend.py

"""
This module provides functionalities for handling Windows Registry using ``reg`` backend.
"""

import subprocess
import tempfile

from pathlib import Path

# user-provided imports
from file_conversor.config import Environment, Log

from file_conversor.system.win import WinRegFile
from file_conversor.backend.abstract_backend import AbstractBackend

LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class WinRegBackend(AbstractBackend):
    """
    A class that provides an interface for handling .REG files using ``reg``.
    """

    SUPPORTED_IN_FORMATS = {
        "reg": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "reg": {},
    }
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
        input_file_or_winreg: str | Path | WinRegFile,
    ):
        """
        Import registry info from input .REG file.

        :param input_file_or_winreg: Input REG file, or WinRegFile.        

        :raises subprocess.CalledProcessError: if reg cannot import registry file
        """
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

    def delete_keys(
        self,
        input_file_or_winreg: str | Path | WinRegFile,
    ):
        """
        Loads registry keys from input .REG file, and deletes them from windows registry.

        :param input_file_or_winreg: Input .REG file.        

        :raises subprocess.CalledProcessError: if reg cannot delete registry keys
        """
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


__all__ = [
    "WinRegBackend",
]
