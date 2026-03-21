# src/file_conversor/gui/_widgets/flow_frame.py

from pathlib import Path
from typing import override

from PySide6.QtWidgets import QFrame, QWidget

from file_conversor.gui._layouts.flow_layout import FlowLayout
from file_conversor.gui._widgets.scrollarea import ScrollArea


class FlowFrame(ScrollArea):

    def __init__(
            self,
            stylesheet_file: Path | None = None,
            spacing: int = 10,
            margins: tuple[int, int, int, int] = (0, 0, 0, 0),
    ) -> None:
        super().__init__(stylesheet_file=stylesheet_file)

        self._layout = FlowLayout(spacing=spacing)
        self._layout.setContentsMargins(*margins)

        frame = QFrame()
        frame.setLayout(self._layout)

        self.setWidget(frame)

    def addWidget(self, *items: QWidget) -> None:
        for item in items:
            self._layout.addWidget(item)

    @override
    def layout(self) -> FlowLayout:
        return self._layout


__all__ = [
    "FlowFrame",
]
