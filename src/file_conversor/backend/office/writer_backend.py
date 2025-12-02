# src\file_conversor\backend\office\writer_backend.py

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation
from file_conversor.backend.office.abstract_libreoffice_backend import AbstractLibreofficeBackend

LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class LibreofficeWriterBackend(AbstractLibreofficeBackend):
    """
    A class that provides an interface for handling doc files using ``writer`` (libreoffice).
    """

    SUPPORTED_IN_FORMATS = {
        "doc": {},
        "docx": {},
        "odt": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "doc": {},
        "docx": {},
        "odt": {},
        "pdf": {},
        "html": {},
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
            install_deps=install_deps,
            verbose=verbose,
        )


__all__ = [
    "LibreofficeWriterBackend",
]
