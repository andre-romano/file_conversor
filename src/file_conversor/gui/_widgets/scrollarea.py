# src/file_conversor/gui/_widgets/scrollarea.py

from pathlib import Path
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QScrollArea, QWidget


class ScrollArea(QScrollArea):
    ScrollBarPolicy = Qt.ScrollBarPolicy

    def __init__(
            self,
            stylesheet_file: Path | None = None,
            scrollbar_width: int = 8,
            scroll_policy: tuple[Qt.ScrollBarPolicy, Qt.ScrollBarPolicy] = (ScrollBarPolicy.ScrollBarAlwaysOff, ScrollBarPolicy.ScrollBarAsNeeded),
    ) -> None:
        super().__init__()
        self._scrollbar_width = scrollbar_width
        self._scroll_policy = scroll_policy

        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(self._scroll_policy[0])
        self.setVerticalScrollBarPolicy(self._scroll_policy[1])

        # set the scrollbar width using stylesheet
        self.setStyleSheet(f"""
            QScrollBar:vertical, QScrollBar:horizontal {{
                width: {self._scrollbar_width}px;                    
            }}
            {stylesheet_file.read_text() if stylesheet_file else ""}
        """)

    def _get_scrollbar_margin(self, policy: ScrollBarPolicy) -> int:
        if policy == self.ScrollBarPolicy.ScrollBarAlwaysOff:
            return 0
        return self._scrollbar_width

    @override
    def setWidget(self, widget: QWidget) -> None:
        super().setWidget(widget)
        # Add a right margin to ensure the scrollbar doesn't overlap the content
        margins = widget.contentsMargins()
        margins.setBottom(margins.bottom() + self._get_scrollbar_margin(self._scroll_policy[0]))
        margins.setRight(margins.bottom() + self._get_scrollbar_margin(self._scroll_policy[1]))
        widget.setContentsMargins(margins)


__all__ = [
    "ScrollArea",
]
