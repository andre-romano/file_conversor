# src/file_conversor/gui/xls/__init__.py

from PySide6.QtWidgets import QFrame


class XlsFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()


__all__ = [
    "XlsFrame",
]
