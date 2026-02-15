# src\file_conversor\backend\office\impress_backend.py

# user-provided imports
from enum import Enum

from file_conversor.backend.office.abstract_libreoffice_backend import (
    AbstractLibreofficeBackend,
)
from file_conversor.config import Log, get_translation


LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class LibreofficeImpressBackend(AbstractLibreofficeBackend):
    """
    A class that provides an interface for handling doc files using ``impress`` (libreoffice).
    """

    class SupportedInFormats(Enum):
        PPT = "ppt"
        PPTX = "pptx"
        ODP = "odp"

    class SupportedOutFormats(Enum):
        PPT = "ppt"
        PPTX = "pptx"
        ODP = "odp"
        PDF = "pdf"

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
    "LibreofficeImpressBackend",
]
