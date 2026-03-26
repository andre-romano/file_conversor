# src/file_conversor/gui/_widgets/sidebar_frame.py

from pathlib import Path
from typing import override

from PySide6.QtWidgets import QFrame, QLayout, QVBoxLayout, QWidget

from file_conversor.gui._utils import Stretch
from file_conversor.gui._widgets import ScrollArea


class SidebarFrame(ScrollArea):
    def __init__(
            self,
            gui_path: Path,
            spacing: int = 0,
            margins: tuple[int, int, int, int] = (0, 0, 0, 0),
    ) -> None:
        stylesheet_file = gui_path / "sidebar.qss"
        assert stylesheet_file.exists(), f"Stylesheet file not found: {stylesheet_file}"

        super().__init__(stylesheet=stylesheet_file.read_text(encoding="utf-8"))

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(*margins)
        self._layout.setSpacing(spacing)

        frame = QFrame()
        frame.setLayout(self._layout)

        self.setWidget(frame)

    def addWidget(self, widget: QWidget) -> None:
        self._layout.addWidget(widget)

    def addLayout(self, layout: QLayout) -> None:
        self._layout.addLayout(layout)

    def addStretch(self, stretch: int = 1) -> None:
        self._layout.addStretch(stretch)

    def addItems(self, *items: QWidget | QLayout | Stretch) -> None:
        for item in items:
            if isinstance(item, QWidget):
                self.addWidget(item)
            elif isinstance(item, Stretch):
                self.addStretch(item.stretch)
            else:
                self.addLayout(item)

    def getStretch(self, stretch: int = 1) -> Stretch:
        return Stretch(stretch)

    @override
    def layout(self) -> QVBoxLayout:
        return self._layout


__all__ = [
    "SidebarFrame",
]
