# src/file_conversor/gui/hash/__init__.py

from PySide6.QtWidgets import QFrame


class HashFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()


__all__ = [
    "HashFrame",
]
