# src/file_conversor/gui/_widgets/qscrollarea.py

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QScrollArea


class ScrollArea(QScrollArea):
    ScrollBarPolicy = Qt.ScrollBarPolicy

    def __init__(
            self,
            size: tuple[int | None, int | None] = (None, None),
            stylesheet_file: Path | None = None,
            scroll_policy: tuple[Qt.ScrollBarPolicy, Qt.ScrollBarPolicy] = (ScrollBarPolicy.ScrollBarAlwaysOff, ScrollBarPolicy.ScrollBarAsNeeded),
    ) -> None:
        super().__init__()

        width, height = size
        if width and width > 0:
            self.setFixedWidth(width + 10)  # adjust for the width of scrollbar when it appears
        if height and height > 0:
            self.setFixedHeight(height + 10)  # adjust for the height of scrollbar when it appears
        if stylesheet_file:
            self.setStyleSheet(stylesheet_file.read_text())
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(scroll_policy[0])
        self.setVerticalScrollBarPolicy(scroll_policy[1])


__all__ = [
    "ScrollArea",
]
