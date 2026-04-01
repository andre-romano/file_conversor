# src\file_conversor\utils\protocols.py

from typing import Any, Callable, Protocol


class CommandProtocol(Protocol):
    def set_progress_callback(self, callback: Callable[[float], Any]) -> None: ...

    def execute(self) -> None: ...


__all__ = [
    "CommandProtocol",
]
