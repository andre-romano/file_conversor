# src/file_conversor/gui/_layouts/grid_layout.py


from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLayout, QWidget


class GridLayout(QGridLayout):
    AlignmentFlag = Qt.AlignmentFlag

    def __init__(
            self,
            cols: int = 3,
            spacing: int = 10,
            margins: tuple[int, int, int, int] = (0, 0, 0, 0),
    ) -> None:
        super().__init__()
        self._cols = cols

        self.setSpacing(spacing)
        self.setContentsMargins(*margins)

    def _get_i_j_pos(self) -> tuple[int, int]:
        k = self.count()
        i, j = divmod(k, self._cols)  # columns
        return i, j

    def _addWidget(self, item: QWidget, i: int, j: int, alignment: Qt.AlignmentFlag | None) -> None:
        if alignment is not None:
            self.addWidget(item, i, j, alignment=alignment)
        else:
            self.addWidget(item, i, j)

    def _addLayout(self, item: QLayout, i: int, j: int, alignment: Qt.AlignmentFlag | None) -> None:
        if alignment is not None:
            self.addLayout(item, i, j, alignment=alignment)
        else:
            self.addLayout(item, i, j)

    def addItems(self, *items: QWidget | QLayout, alignment: Qt.AlignmentFlag | None = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter) -> None:
        for item in items:
            i, j = self._get_i_j_pos()
            if isinstance(item, QWidget):
                self._addWidget(item, i, j, alignment)
            else:
                self._addLayout(item, i, j, alignment)


__all__ = [
    "GridLayout",
]
