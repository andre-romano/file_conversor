# src/file_conversor/gui/_widgets/sidebar_frame.py

from pathlib import Path
from typing import override

from PySide6.QtWidgets import QFrame, QVBoxLayout

from file_conversor.gui._widgets.scrollarea import ScrollArea


class SidebarFrame(ScrollArea):
    def __init__(
            self,
            gui_path: Path,
            spacing: int = 0,
            margins: tuple[int, int, int, int] = (0, 0, 0, 0),
    ) -> None:
        super().__init__(stylesheet_file=gui_path / "sidebar.qss")

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(*margins)
        self._layout.setSpacing(spacing)

        frame = QFrame()
        frame.setLayout(self._layout)

        self.setWidget(frame)

    @override
    def layout(self) -> QVBoxLayout:
        return self._layout


__all__ = [
    "SidebarFrame",
]
