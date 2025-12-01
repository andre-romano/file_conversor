# src\file_conversor\backend\http_backend.py

"""
This module provides functionalities for handling repositories using HTTP.
"""

import requests
import requests_cache

from pathlib import Path
from typing import Any, Callable, Iterable

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.config import Environment, Configuration, Log, get_translation

from file_conversor.utils.validators import check_file_format

_ = get_translation()
LOG = Log.get_instance()
CONFIG = Configuration.get_instance()

logger = LOG.getLogger(__name__)


class HttpBackend(AbstractBackend):
    """
    HttpBackend is a class that provides an interface for handling HTTP requests.
    """

    SUPPORTED_IN_FORMATS = {}

    SUPPORTED_OUT_FORMATS = {}

    EXTERNAL_DEPENDENCIES = set()

    __instance = None

    @classmethod
    def get_instance(
        cls,
        verbose: bool = False,
    ):
        """
        Initialize instance

        :param verbose: Verbose logging. Defaults to False.
        :param cache: Enable caching. Defaults to True.
        """
        if not cls.__instance:
            cls.__instance = cls()
        cls.__instance._verbose = verbose
        return cls.__instance

    def __init__(
        self,
        verbose: bool = False,
    ):
        """
        Initialize the backend.

        :param verbose: Verbose logging. Defaults to False.    
        :param cache_enabled: Enable caching. Defaults to True.  
        :param cache_name: Name of the cache file. Defaults to ".http_cache".  
        :param cache_expire_after: Cache expiration time in seconds. Defaults to 1 day
        """
        super().__init__()
        self._verbose = verbose
        self._cache_file = Environment.get_data_folder() / ".http_cache.sqlite"

        # Creates a persistent SQLite cache file: http_cache.sqlite
        requests_cache.install_cache(
            cache_name=str(self._cache_file.with_suffix("").resolve()),
            backend="sqlite",
            expire_after=int(CONFIG["cache-expire-after"]),
            allowable_codes=(200,),  # ONLY cache successful HTTP 200 responses
            stale_if_error=True,     # Use stale cache if network error occurs
            old_data_on_error=True,  # Use old cache data if http 500 error occurs
            fast_save=True,          # Faster cache saving
        )

    def clear_cache(self):
        """Clear the HTTP cache."""
        requests_cache.clear()
        logger.warning(_("HTTP cache cleared."))

    def get_json(
        self,
        url: str,
        **kwargs,
    ) -> Any:
        """Get JSON data from a URL.

        :param url: The URL to fetch the JSON data from.        
        :param kwargs: Additional arguments to pass to the requests.get() method.
        :return: The JSON data.

        :raises RuntimeError: if the request fails or the response is not JSON.
        """
        response = requests.get(url, **kwargs)
        if not response.ok:
            raise RuntimeError(f"{_('Failed to get JSON from url')} '{url}': {response.status_code} - {response.text}")
        try:
            return response.json()
        except Exception as e:
            raise RuntimeError(f"{_('Failed to parse JSON from url')} '{url}': {e}")

    def download(
        self,
        url: str,
        dest_file: str | Path,
        progress_callback: Callable[[float], Any] | None = None,
    ):
        """
        Download a file from a URL.
        """
        dest_file = Path(dest_file).resolve()
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        downloaded_bytes = 0.0

        with requests.get(url, stream=True) as response:
            if not response.ok:
                raise RuntimeError(f"{_('Failed to download file')}: {response.status_code} - {response.text}")
            total_size = float(response.headers.get("content-length", 0))
            with dest_file.open("wb") as f:
                for data in response.iter_content(chunk_size=1024):
                    f.write(data)
                    downloaded_bytes += len(data)
                    if progress_callback:
                        progress_callback(downloaded_bytes / total_size * 100)
        if not dest_file.exists():
            raise RuntimeError(f"{_('Failed to download file')}: '{dest_file}'")
