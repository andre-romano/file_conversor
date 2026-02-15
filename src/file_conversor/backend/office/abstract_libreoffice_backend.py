# src\file_conversor\backend\office\abstract_libreoffice_backend.py

from pathlib import Path
from typing import override

from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.backend.office._convert_protocol import ConvertProtocol

# user-provided imports
from file_conversor.config import Environment, Log, get_translation
from file_conversor.dependency import BrewPackageManager, ScoopPackageManager


LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AbstractLibreofficeBackend(AbstractBackend, ConvertProtocol):
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
                    rf"{Path.home()}\scoop\apps\libreoffice\current\LibreOffice\program"
                ]),
                BrewPackageManager({
                    "soffice": "libreoffice"
                }),
            },
            install_answer=install_deps,
        )
        self._verbose = verbose

        self._libreoffice_bin = self.find_in_path("soffice")

    @override
    def convert(
        self,
        input_path: Path,
        output_path: Path,
    ):
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
        if any(p.startswith("Error:") for p in (process.stdout or "", process.stderr or "")):
            raise RuntimeError(f"LibreOffice conversion failed: {process.stdout or ''} {process.stderr or ''}")


__all__ = [
    "AbstractLibreofficeBackend",
]
