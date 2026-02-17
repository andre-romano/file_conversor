# src/file_conversor/gui/image/__init__.py
from PySide6.QtWidgets import QFrame


class ImageFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()


__all__ = [
    "ImageFrame",
]
