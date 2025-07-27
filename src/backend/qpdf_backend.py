# src/backend/qpdf_backend.py

"""
This module provides functionalities for handling PDF files using ``qpdf`` backend.
"""

import os
import shutil
import subprocess


from typing import Iterable

# user-provided imports
from backend.abstract_backend import AbstractBackend
from dependency import BrewPackageManager, ScoopPackageManager


class QPDFBackend(AbstractBackend):
    """
    A class that provides an interface for handling PDF files using ``qpdf``.
    """

    @staticmethod
    def check_file_exists(filename: str):
        """
        Check if `filename` exists

        :raises FileNotFoundError: if file not found
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File '{filename}' not found")

    def __init__(
        self,
        install_deps: bool | None = None,
        verbose: bool = False,
    ):
        """
        Initialize the ``qpdf`` backend

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action. Defaults to None.      

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

        qpdf_bin = shutil.which("qpdf")
        self._qpdf_bin = qpdf_bin if qpdf_bin else "QPDF_NOT_FOUND"

    def repair(
        self,
        input_file: str,
        output_file: str,
        decrypt_password: str | None = None,
    ) -> subprocess.Popen:
        """
        Repair input PDF file.

        :param input_files: Input PDF file. 
        :param output_files: Output PDF file.
        :param decryption_password: Decryption password for input PDF file. Defaults to None (do not decrypt).

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        # build command
        command = []
        command.extend([self._qpdf_bin])
        if decrypt_password:
            command.extend([f"--password={decrypt_password}", "--decrypt"])
        command.extend(["--linearize", input_file, output_file])

        # Execute command
        print("Executing QPDF:")
        print(" ".join(command))
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        return process
