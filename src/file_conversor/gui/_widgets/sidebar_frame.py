# src/file_conversor/gui/_widgets/sidebar_frame.py

from pathlib import Path
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QScrollArea, QVBoxLayout


class SidebarFrame(QScrollArea):
    ScrollBarPolicy = Qt.ScrollBarPolicy

    def __init__(
            self,
            gui_path: Path,
            width: int,
            margins: tuple[int, int, int, int] = (0, 0, 0, 0),
            spacing: int = 0,
            scroll_policy: tuple[Qt.ScrollBarPolicy, Qt.ScrollBarPolicy] = (ScrollBarPolicy.ScrollBarAlwaysOff, ScrollBarPolicy.ScrollBarAsNeeded),
    ) -> None:
        super().__init__()
        stylesheet_file = gui_path / "sidebar.qss"

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(*margins)
        self._layout.setSpacing(spacing)

        frame = QFrame()
        frame.setFixedWidth(width)
        frame.setLayout(self._layout)

        self.setWidgetResizable(True)
        self.setStyleSheet(stylesheet_file.read_text())
        self.setFixedWidth(width + 10)  # adjust for the width of scrollbar when it appears
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(scroll_policy[0])
        self.setVerticalScrollBarPolicy(scroll_policy[1])
        self.setWidget(frame)

    @override
    def layout(self) -> QVBoxLayout:
        return self._layout


__all__ = [
    "SidebarFrame",
]
