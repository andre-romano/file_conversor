# src/file_conversor/gui/_widgets/form_frame.py

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLayout,
    QVBoxLayout,
    QWidget,
)

from file_conversor.gui._frames.statusbar_frame import StatusBarFrame
from file_conversor.gui._widgets import Label, PushButton, ScrollArea


class FormFrame(QFrame):
    def __init__(
        self,
        gui_path: Path,
        title: str,
        title_stylesheet: str = "font-size: 18px; font-weight: bold;",
        spacing: tuple[int, int] = (5, 10),
        margins: tuple[int, int, int, int] = (10, 10, 10, 10),
    ) -> None:
        super().__init__()
        title_label = Label(text=title, stylesheet=title_stylesheet)

        self._form_layout = QFormLayout()
        self._form_layout.setHorizontalSpacing(spacing[0])
        self._form_layout.setVerticalSpacing(spacing[1])
        self._form_layout.setContentsMargins(0, 0, 0, 0)

        form_frame = QFrame()
        form_frame.setLayout(self._form_layout)

        scrollarea = ScrollArea()
        scrollarea.setWidget(form_frame)

        self.status_bar = StatusBarFrame(gui_path=gui_path)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(spacing[1])
        content_layout.setContentsMargins(*margins)
        content_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        content_layout.addWidget(scrollarea, stretch=1)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(content_layout, stretch=1)
        layout.addWidget(self.status_bar)

        self.setLayout(layout)

        self._confirm_btn = PushButton()
        self._confirm_btn.clicked.connect(self.on_confirm_clicked)

    def addRow(self, label: str | QWidget, widget: QWidget | QLayout) -> None:
        self._form_layout.addRow(label, widget)

    def addConfirmButton(self, text: str) -> None:
        self._confirm_btn.setText(text)

        confirm_layout = QHBoxLayout()
        confirm_layout.setSpacing(0)
        confirm_layout.setContentsMargins(0, 0, 0, 0)
        confirm_layout.addStretch()
        confirm_layout.addWidget(self._confirm_btn)
        self._form_layout.addRow(confirm_layout)

    def on_confirm_clicked(self) -> None:
        raise NotImplementedError("Subclasses must implement this method.")


__all__ = [
    "FormFrame",
]
