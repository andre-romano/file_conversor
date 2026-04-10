# src/file_conversor/gui/_widgets/bitrate.py


from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QLineEdit

from file_conversor.config import get_translation


_ = get_translation()


class BitrateWidget(QLineEdit):
    def __init__(self, bitrate: int | None) -> None:
        super().__init__(
            placeholderText=_("Bitrate (kbps)"),
            clearButtonEnabled=True,
        )
        self.setValidator(QIntValidator(1, 999999, self))
        self.setText(str(bitrate) if bitrate is not None else "")

    def get_bitrate(self) -> int | None:
        data = self.text().strip()
        return int(data) if data else None


__all__ = [
    "BitrateWidget",
]
