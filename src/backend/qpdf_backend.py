# src/backend/qpdf_backend.py

"""
This module provides functionalities for handling PDF files using ``qpdf`` backend.
"""

import shutil
import subprocess

# user-provided imports
from config.log import Log

from dependency import BrewPackageManager, ScoopPackageManager
from backend.abstract_backend import AbstractBackend

LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class QPDFBackend(AbstractBackend):
    """
    A class that provides an interface for handling PDF files using ``qpdf``.
    """

    SUPPORTED_IN_FORMATS = {
        "pdf": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "pdf": {},
    }

    def __init__(
        self,
        install_deps: bool | None,
        verbose: bool = False,
    ):
        """
        Initialize the ``qpdf`` backend

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action.

        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__(
            pkg_managers={
                ScoopPackageManager({
                    "qpdf": "qpdf"
                }),
                BrewPackageManager({
                    "qpdf": "qpdf"
                }),
            },
            install_answer=install_deps,
        )
        self._verbose = verbose

        self._qpdf_bin = self.find_in_path("qpdf")

    def repair(
        self,
        input_file: str,
        output_file: str,
        decrypt_password: str | None = None,
        compress: bool = True,
    ) -> subprocess.Popen:
        """
        Repair input PDF file.

        :param input_files: Input PDF file. 
        :param output_files: Output PDF file.
        :param decryption_password: Decryption password for input PDF file. Defaults to None (do not decrypt).
        :param compress: Compress PDF output file structures. Defaults to True (compress structures, losslessly).

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        # build command
        command = []
        command.extend([str(self._qpdf_bin)])
        if compress:
            command.extend(["--object-streams=generate", "--compress-streams=y", "--stream-data=compress"])
        if decrypt_password:
            command.extend([f"--password={decrypt_password}", "--decrypt"])
        command.extend(["--linearize", input_file, output_file])

        # Execute command
        logger.info("Executing QPDF ...")
        logger.debug(" ".join(command))
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        return process
