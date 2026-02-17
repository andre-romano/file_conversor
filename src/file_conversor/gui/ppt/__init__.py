# src/file_conversor/gui/ppt/__init__.py
from PySide6.QtWidgets import QFrame


class PptFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()


__all__ = [
    "PptFrame",
]
