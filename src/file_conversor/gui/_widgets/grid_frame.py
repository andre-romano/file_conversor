# src/file_conversor/gui/_widgets/sidebar_frame.py

from pathlib import Path
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QLayout, QWidget

from file_conversor.gui._widgets.scrollarea import ScrollArea


class GridFrame(ScrollArea):
    AlignmentFlag = Qt.AlignmentFlag

    def __init__(
            self,
            stylesheet_file: Path | None = None,
            cols: int = 3,
            spacing: int = 10,
            margins: tuple[int, int, int, int] = (0, 0, 0, 0),
    ) -> None:
        super().__init__(stylesheet_file=stylesheet_file)
        self._cols = cols

        self._layout = QGridLayout()
        self._layout.setSpacing(spacing)
        self._layout.setContentsMargins(*margins)

        frame = QFrame()
        frame.setLayout(self._layout)

        self.setWidget(frame)

    def addItems(self, *items: QWidget | QLayout, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter) -> None:
        for k, item in enumerate(items):
            i, j = divmod(k, self._cols)  # columns
            i += self._layout.rowCount()
            j += self._layout.columnCount()
            if isinstance(item, QWidget):
                self._layout.addWidget(item, i, j, alignment=alignment)
            else:
                self._layout.addLayout(item, i, j, alignment=alignment)

    @override
    def layout(self) -> QGridLayout:
        return self._layout


__all__ = [
    "GridFrame",
]
