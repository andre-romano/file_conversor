# src\file_conversor\backend\office\writer_backend.py

# user-provided imports
from enum import StrEnum

from file_conversor.backend.office.abstract_libreoffice_backend import (
    AbstractLibreofficeBackend,
)
from file_conversor.config import LOG, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


class LibreofficeWriterBackend(AbstractLibreofficeBackend):
    """
    A class that provides an interface for handling doc files using ``writer`` (libreoffice).
    """

    class SupportedInFormats(StrEnum):
        DOC = "doc"
        DOCX = "docx"
        ODT = "odt"

    class SupportedOutFormats(StrEnum):
        PDF = "pdf"
        DOCX = "docx"
        DOC = "doc"
        ODT = "odt"
        HTML = "html"

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
