# src/file_conversor/gui/_widgets/card.py

from pathlib import Path
from typing import override

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy, QVBoxLayout

from file_conversor.gui._widgets.label import Label, LabelImage


class Card(QFrame):
    clicked = Signal()

    def __init__(
        self,
        icon_path: Path,
        title: str,
        description: str,
        gui_path: Path,
        max_size: tuple[int, int] = (180, 100),
    ):
        super().__init__()
        stylesheet_file = gui_path / "card.qss"
        assert stylesheet_file.exists(), f"Stylesheet not found: {stylesheet_file}"

        self.setStyleSheet(stylesheet_file.read_text(encoding="utf-8"))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # guarantee the card doesn't expand too much
        self.setMaximumSize(*max_size)  # set the maximum size of the widget
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)  # set the size policy to maximum to prevent expansion

        # main layout - horizontal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.icon_label = LabelImage(
            name="icon_label",
            image=icon_path,
            size=(32, 32),
            alignment=Label.AlignmentFlag.AlignCenter,
        )

        # text layout - vertical
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        self.title_label = Label(
            name="title_label",
            text=title,
        )

        self.desc_label = Label(
            name="desc_label",
            text=description,
            word_wrap=True,
            alignment=Label.AlignmentFlag.AlignTop | Label.AlignmentFlag.AlignCenter
        )

        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.desc_label)
        text_layout.addStretch()

        # add to main layout
        layout.addWidget(self.icon_label)
        layout.addLayout(text_layout)

    @override
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)


__all__ = [
    "Card",
]
