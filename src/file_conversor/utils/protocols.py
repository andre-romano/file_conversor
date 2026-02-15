# src\file_conversor\utils\protocols.py

from typing import Iterable, Protocol


class BackendProtocol(Protocol):
    @classmethod
    def get_external_dependencies(cls) -> Iterable[str]:
        """ Return a list of external dependencies required by the backend."""
        ...

    @classmethod
    def get_supported_in_formats(cls) -> Iterable[str]:
        """ Return a list of supported input formats by the backend."""
        ...

    @classmethod
    def get_supported_out_formats(cls) -> Iterable[str]:
        """ Return a list of supported output formats by the backend."""
        ...


__all__ = [
    "BackendProtocol",
]
