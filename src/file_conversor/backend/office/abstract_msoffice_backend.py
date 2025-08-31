# src\file_conversor\backend\office\abstract_msoffice_backend.py

from pathlib import Path

# user-provided imports
from file_conversor.config import Log
from file_conversor.config.locale import get_translation

from file_conversor.backend.abstract_backend import AbstractBackend

from file_conversor.system import CURR_PLATFORM, PLATFORM_WINDOWS

# conditional import
if CURR_PLATFORM == PLATFORM_WINDOWS:
    import pythoncom  # pyright: ignore[reportMissingModuleSource]
    from win32com import client  # pyright: ignore[reportMissingModuleSource]
else:
    pythoncom = None
    client = None

LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class Win32Com:
    def __init__(self, prog_id, visible: bool | None = None):
        """
        Win32Com dispatch wrapper class

        prog_id: The registered COM program name, e.g., 'Word.Application'
        visible: Set to True to make the application visible. Defaults to None.
        """
        super().__init__()
        self._prog_id = prog_id
        self._visible = visible
        self._app = None

    def __enter__(self):
        if not client:
            raise OSError("Win32Com is only available in Windows OS")
        self._app = client.Dispatch(self._prog_id)
        try:
            if self._visible is not None:
                self._app.Visible = self._visible
        except AttributeError:
            pass  # Some COM objects don't have Visible
        return self._app

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._app:
                self._app.Quit()
        except Exception:
            logger.warning(f"Fail to quit Win32Com prog_id '{self._prog_id}'. Try again later.")
        self._app = None
        # Returning False means exceptions (if any) will propagate
        return False


class AbstractMSOfficeBackend(AbstractBackend):
    """
    A class that provides an interface for handling files using ``msoffice``.
    """

    def __init__(
        self,
        prog_id: str,
        install_deps: bool | None,
        verbose: bool = False,
    ):
        """
        Initialize the backend

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action. 

        :param verbose: Verbose logging. Defaults to False.      
        """
        super().__init__()
        self._verbose = verbose
        self.PROG_ID = prog_id

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
        :raises OSError: if os is not Windows, or MS Office App not available.
        """
        raise NotImplementedError("Must be implemented within a subclass")

    def is_available(self) -> bool:
        """Returns True if MS Office App is available, False otherwise"""
        if not pythoncom:
            return False
        try:
            pythoncom.CoInitialize()
            clsid = pythoncom.ProgIDFromCLSID(self.PROG_ID)
            return clsid is not None
        except:
            logger.warning(f"Microsoft Office '{self.PROG_ID}' backend not available.")
            return False
        finally:
            pythoncom.CoUninitialize()
