# src/file_conversor/gui/_widgets/output_format.py


from typing import Iterable

from PySide6.QtWidgets import QComboBox

from file_conversor.config import get_translation


_ = get_translation()


class OutputFormatWidget(QComboBox):
    def __init__(self, extensions: Iterable[str]) -> None:
        super().__init__()
        for suffix in extensions:
            ext = suffix.lstrip(".")
            self.addItem(ext.upper(), ext.lower())
        self.setCurrentIndex(0)

    def get_format(self) -> str:
        return self.currentData()


__all__ = [
    "OutputFormatWidget",
]
