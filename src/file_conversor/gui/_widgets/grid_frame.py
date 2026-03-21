# src/file_conversor/gui/_widgets/grid_frame.py

from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QLayout, QWidget

from file_conversor.gui._widgets.scrollarea import ScrollArea


class GridFrame(ScrollArea):
    AlignmentFlag = Qt.AlignmentFlag

    def __init__(
            self,
            stylesheet: str = "",
            cols: int = 3,
            spacing: int = 10,
            margins: tuple[int, int, int, int] = (0, 0, 0, 0),
    ) -> None:
        super().__init__(stylesheet=stylesheet)
        self._cols = cols

        self._layout = QGridLayout()
        self._layout.setSpacing(spacing)
        self._layout.setContentsMargins(*margins)

        frame = QFrame()
        frame.setLayout(self._layout)

        self.setWidget(frame)

    def _get_i_j_pos(self) -> tuple[int, int]:
        k = self._layout.count()
        i, j = divmod(k, self._cols)  # columns
        return i, j

    def addWidget(self, item: QWidget, alignment: Qt.AlignmentFlag | None = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter) -> None:
        i, j = self._get_i_j_pos()
        if alignment is not None:
            self._layout.addWidget(item, i, j, alignment=alignment)
        else:
            self._layout.addWidget(item, i, j)

    def addLayout(self, item: QLayout, alignment: Qt.AlignmentFlag | None = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter) -> None:
        i, j = self._get_i_j_pos()
        if alignment is not None:
            self._layout.addLayout(item, i, j, alignment=alignment)
        else:
            self._layout.addLayout(item, i, j)

    def addItems(self, *items: QWidget | QLayout, alignment: Qt.AlignmentFlag | None = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter) -> None:
        for item in items:
            if isinstance(item, QWidget):
                self.addWidget(item, alignment=alignment)
            else:
                self.addLayout(item, alignment=alignment)

    @override
    def layout(self) -> QGridLayout:
        return self._layout


__all__ = [
    "GridFrame",
]
