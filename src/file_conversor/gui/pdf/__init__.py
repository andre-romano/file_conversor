# src/file_conversor/gui/pdf/__init__.py

from PySide6.QtWidgets import QFrame


class PdfFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()


__all__ = [
    "PdfFrame",
]
