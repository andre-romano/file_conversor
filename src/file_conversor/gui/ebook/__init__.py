# src/file_conversor/gui/ebook/__init__.py

from PySide6.QtWidgets import QFrame


class EbookFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()


__all__ = [
    "EbookFrame",
]
