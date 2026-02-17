# src/file_conversor/gui/config/__init__.py

from PySide6.QtWidgets import QFrame


class ConfigFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()


__all__ = [
    "ConfigFrame",
]
