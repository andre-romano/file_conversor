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

from file_conversor.config import Configuration, State, Environment, Log, AbstractSingletonThreadSafe, get_translation

from file_conversor.utils.validators import check_file_format

_ = get_translation()
LOG = Log.get_instance()
CONFIG = Configuration.get_instance()

logger = LOG.getLogger(__name__)


class NetworkError(RuntimeError):
    """Base exception for network-related errors in HttpBackend."""


class HttpBackend(AbstractBackend, AbstractSingletonThreadSafe):
    """
    HttpBackend is a class that provides an interface for handling HTTP requests.
    """

    SUPPORTED_IN_FORMATS = {}

    SUPPORTED_OUT_FORMATS = {}

    EXTERNAL_DEPENDENCIES = set()

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
        self._cached_session = requests_cache.CachedSession(
            cache_name=str(self._cache_file.with_suffix("").resolve()),
            backend="sqlite",
            expire_after=int(CONFIG["cache-expire-after"]),
            allowable_codes=(200,),  # ONLY cache successful HTTP 200 responses
            stale_if_error=True,     # Use stale cache if network error occurs
            old_data_on_error=True,  # Use old cache data if http 500 error occurs
            fast_save=True,          # Faster cache saving
        )
        self._plain_session = requests.Session()

    def clear_cache(self):
        """Clear the HTTP cache."""
        requests_cache.clear()
        logger.warning(_("HTTP cache cleared."))

    def get_json(
        self,
        url: str,
        cache_enabled: bool = True,
        timeout: tuple[int, int] | None = (5, 10),
        **kwargs,
    ) -> Any:
        """Get JSON data from a URL.

        :param url: The URL to fetch the JSON data from.        
        :param cache_enabled: Whether to use the cache. Defaults to True.
        :param timeout: A tuple specifying the connection and read timeout in seconds. Defaults to (5,30).
        :param kwargs: Additional arguments to pass to the requests.get() method.
        :return: The JSON data.

        :raises NetworkError: if the request fails or the response is not JSON.
        """
        session = self._cached_session if cache_enabled else self._plain_session
        try:
            response = session.get(url, timeout=timeout, **kwargs)
            if not response.ok:
                raise NetworkError(f"Response code: {response.status_code} - {response.text}")
            return response.json()
        except Exception as e:
            raise NetworkError(f"{_('Error during JSON fetch from url')} '{url}': {repr(e)}")

    def download(
        self,
        url: str,
        dest_file: str | Path,
        cache_enabled: bool = False,
        timeout: tuple[int, int] | None = (5, 600),
        progress_callback: Callable[[float], Any] | None = None,
        **kwargs,
    ):
        """
        Download a file from a URL.

        :param url: The URL to download the file from.
        :param dest_file: The destination file path.
        :param cache_enabled: Whether to use the cache. Defaults to False.
        :param timeout: A tuple specifying the connection and read timeout in seconds. Defaults to (5,600).
        :param progress_callback: A callback function to report download progress (0-100). Defaults to None.
        :param kwargs: Additional arguments to pass to the requests.get() method.

        :raises NetworkError: if the download fails.
        """
        dest_file = Path(dest_file).resolve()
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        downloaded_bytes = 0.0

        session = self._cached_session if cache_enabled else self._plain_session
        try:
            with session.get(url, timeout=timeout, stream=True, **kwargs) as response:
                if not response.ok:
                    raise NetworkError(f"{_('Response code')}: {response.status_code} - {response.text}")
                total_size = float(response.headers.get("content-length", 0))
                with dest_file.open("wb") as f:
                    for data in response.iter_content(chunk_size=1024):
                        f.write(data)
                        downloaded_bytes += len(data)
                        if progress_callback:
                            progress_callback(downloaded_bytes / total_size * 100)
            if not dest_file.exists():
                raise FileNotFoundError(f"'{dest_file}'")
        except Exception as e:
            raise NetworkError(f"{_('Network error during download')}: {repr(e)}")


__all__ = [
    "NetworkError",
    "HttpBackend",
]
