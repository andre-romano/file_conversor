# src/file_conversor/gui/_layouts/flow_layout.py

from dataclasses import dataclass
from typing import override

from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtWidgets import QLayout, QLayoutItem, QWidget


@dataclass
class _RowItem:
    items: list[QLayoutItem]
    width: int
    height: int


class FlowLayout(QLayout):
    """A custom layout that wraps its items like words in a paragraph."""

    def __init__(
        self,
        parent: QWidget | None = None,
        spacing: int = 10,
        margins: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        super().__init__(parent)
        self._item_list: list[QLayoutItem] = []
        self.setSpacing(spacing)
        self.setContentsMargins(*margins)

    def __del__(self):
        while self.count() > 0:
            self.takeAt(0)

    def addItems(self, *items: QWidget) -> None:
        for item in items:
            self.addWidget(item)

    @override
    def addItem(self, item: QLayoutItem) -> None:
        self._item_list.append(item)

    @override
    def count(self) -> int:
        return len(self._item_list)

    @override
    def itemAt(self, index: int) -> QLayoutItem | None:
        if 0 <= index < len(self._item_list):
            return self._item_list[index]
        return None

    @override
    def takeAt(self, index: int) -> QLayoutItem:
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)
        raise IndexError("Index out of range")

    @override
    def expandingDirections(self):
        return Qt.Orientation(0)

    @override
    def hasHeightForWidth(self):
        return True

    @override
    def heightForWidth(self, width: int):
        # Calculates the height needed for a given width (this is the magic wrapping part)
        return self._doLayout(QRect(0, 0, width, 0), True)

    @override
    def setGeometry(self, rect: QRect):
        super().setGeometry(rect)
        self._doLayout(rect, False)

    @override
    def sizeHint(self):
        return self.minimumSize()

    @override
    def minimumSize(self):
        size = QSize()
        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def _createRows(self, rows: list[_RowItem], rect: QRect) -> None:
        """ Groups items into rows and calculates the total height needed. Also applies horizontal centering within each row."""
        current_row_items: list[QLayoutItem] = []
        current_row_width: int = 0
        current_row_height: int = 0

        for item in self._item_list:
            item_width = item.sizeHint().width()
            item_height = item.sizeHint().height()

            # If adding this item exceeds the width of the layout
            if current_row_items and (current_row_width + item_width > rect.width()):
                # Save the completed row
                rows.append(_RowItem(
                    items=current_row_items,
                    width=current_row_width - self.spacing(),  # Remove trailing space
                    height=current_row_height
                ))
                # Reset variables for the new row
                current_row_items = []
                current_row_width = 0
                current_row_height = 0

            # Add the item to the current row
            current_row_items.append(item)
            current_row_width += item_width + self.spacing()
            current_row_height = max(current_row_height, item_height)

        # Don't forget to save the very last row!
        if current_row_items:
            rows.append(_RowItem(
                items=current_row_items,
                width=current_row_width - self.spacing(),
                height=current_row_height
            ))

    def _getStartY(self, rows: list[_RowItem], rect: QRect) -> tuple[int, int]:
        """Calculates the starting Y position for vertical centering."""
        # 1. Sum the height of all rows, plus the spacing between them
        total_content_height = sum(row.height for row in rows) + max(0, (len(rows) - 1) * self.spacing())

        # 2. Calculate the starting Y position
        start_y = rect.y()

        # Only center vertically if the window is taller than the content.
        # If the content is taller (needs scrolling), we MUST start at the top so it doesn't push up out of bounds.
        if total_content_height < rect.height():
            start_y += round((rect.height() - total_content_height) / 2.0)
        return start_y, total_content_height

    def _layoutItems(self, rows: list[_RowItem], rect: QRect, start_y: int, test_only: bool) -> None:
        current_y: int = start_y
        for row in rows:
            # Horizontal centering offset for this specific row
            offset_x = rect.x()
            if row.width < rect.width():
                offset_x += round((rect.width() - row.width) / 2.0)

            if not test_only:
                for item in row.items:
                    item.setGeometry(QRect(QPoint(offset_x, current_y), item.sizeHint()))
                    offset_x += item.sizeHint().width() + self.spacing()

            # Move down to the next row
            current_y += row.height + self.spacing()

    def _doLayout(self, rect: QRect, test_only: bool) -> int:
        """Calculates rows, applies vertical and horizontal centering."""
        rows: list[_RowItem] = []

        # --- PHASE 1: Group items into rows and calculate total height ---
        self._createRows(rows, rect)

        # --- PHASE 2: Calculate Vertical Centering Offset ---
        start_y, total_content_height = self._getStartY(rows, rect)

        # --- PHASE 3: Position the items on screen ---
        self._layoutItems(rows, rect, start_y, test_only)

        # Return the total height used (required by the Qt Layout Engine)
        return total_content_height


__all__ = [
    "FlowLayout",
]
