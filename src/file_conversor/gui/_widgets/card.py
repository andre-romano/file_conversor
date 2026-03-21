# src/file_conversor/gui/_widgets/card.py

from pathlib import Path
from typing import override

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy, QVBoxLayout

from file_conversor.gui._widgets.label import Label, LabelImage


class Card(QFrame):
    clicked = Signal()

    def __init__(
        self,
        icon: Path | QIcon,
        title: str,
        description: str,
        gui_path: Path,
        stylesheet: str = "",
        icon_size: tuple[int, int] = (46, 46),
        max_size: tuple[int, int] = (180, 90),
    ):
        super().__init__()
        stylesheet_file = gui_path / "card.qss"
        assert stylesheet_file.exists(), f"Stylesheet not found: {stylesheet_file}"

        self.setStyleSheet(f"""
            {stylesheet_file.read_text(encoding="utf-8")}
            {stylesheet}    
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # guarantee the card doesn't expand too much
        self.setFixedWidth(max_size[0])  # set the fixed width of the widget
        self.setMaximumSize(*max_size)  # set the maximum size of the widget
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)  # set the size policy to maximum to prevent expansion

        # main layout
        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(8, 10, 8, 10)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # title layout
        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.icon_label = LabelImage(
            name="icon_label",
            image=icon,
            size=icon_size,
            alignment=Label.AlignmentFlag.AlignHCenter | Label.AlignmentFlag.AlignVCenter,
        )

        self.title_label = Label(
            name="title_label",
            text=title,
            alignment=Label.AlignmentFlag.AlignLeft | Label.AlignmentFlag.AlignBottom,
        )

        self.desc_label = Label(
            name="desc_label",
            text=description,
            word_wrap=True,
            alignment=Label.AlignmentFlag.AlignJustify | Label.AlignmentFlag.AlignTop,
        )

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.desc_label)

        # add to main layout
        layout.addWidget(self.icon_label)
        layout.addLayout(title_layout, stretch=1)
        self.setLayout(layout)

    @override
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)


__all__ = [
    "Card",
]
