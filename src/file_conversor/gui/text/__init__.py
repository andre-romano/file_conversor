# src/file_conversor/gui/text/__init__.py

from PySide6.QtWidgets import QFrame


class TextFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()


__all__ = [
    "TextFrame",
]
