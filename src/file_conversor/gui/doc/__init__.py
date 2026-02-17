# src/file_conversor/gui/doc/__init__.py
from PySide6.QtWidgets import QFrame


class DocFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()


__all__ = [
    "DocFrame",
]
