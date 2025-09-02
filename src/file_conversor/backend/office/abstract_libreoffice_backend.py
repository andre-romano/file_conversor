# src\file_conversor\backend\office\abstract_libreoffice_backend.py

from pathlib import Path

# user-provided imports
from file_conversor.config import Environment, Log
from file_conversor.config.locale import get_translation

from file_conversor.backend.abstract_backend import AbstractBackend

from file_conversor.dependency.brew_pkg_manager import BrewPackageManager
from file_conversor.dependency.scoop_pkg_manager import ScoopPackageManager

LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AbstractLibreofficeBackend(AbstractBackend):
    """
    A class that provides an interface for handling files using ``libreoffice``.
    """
    EXTERNAL_DEPENDENCIES = {
        "soffice",
    }

    def __init__(
        self,
        install_deps: bool | None,
        verbose: bool = False,
    ):
        """
        Initialize the backend

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action. 

        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__(
            pkg_managers={
                ScoopPackageManager({
                    "soffice": "libreoffice"
                }, buckets=[
                    "extras",
                ], env=[
                    r"C:\Users\Andre\scoop\apps\libreoffice\current\LibreOffice\program"
                ]),
                BrewPackageManager({
                    "soffice": "libreoffice"
                }),
            },
            install_answer=install_deps,
        )
        self._verbose = verbose

        self._libreoffice_bin = self.find_in_path("soffice")

    def convert(
        self,
        output_file: str | Path,
        input_file: str | Path,
    ):
        """
        Convert input file into an output file.

        :param output_file: Output file.
        :param input_file: Input file.        

        :raises FileNotFoundError: if input file not found.
        """
        self.check_file_exists(input_file)

        input_path = Path(input_file).resolve()
        output_path = Path(output_file).resolve()

        output_dir = output_path.parent
        output_format = output_path.suffix.lstrip(".").lower()

        # Execute command
        process = Environment.run(
            str(self._libreoffice_bin),
            "--headless",
            "--convert-to",
            str(output_format),
            "--outdir",
            str(output_dir),
            str(input_path)
        )
        return process
