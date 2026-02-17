# src/file_conversor/gui/audio/__init__.py
from PySide6.QtWidgets import QFrame


class AudioFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()


__all__ = [
    "AudioFrame",
]
