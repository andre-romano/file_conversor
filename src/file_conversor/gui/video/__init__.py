# src/file_conversor/gui/video/__init__.py
from PySide6.QtWidgets import QFrame


class VideoFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()


__all__ = [
    "VideoFrame",
]
