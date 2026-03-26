# src/file_conversor/gui/_widgets/form_frame.py

from PySide6.QtWidgets import QFormLayout, QFrame, QHBoxLayout, QLayout, QWidget

from file_conversor.gui._widgets import Label, PushButton, ScrollArea


class FormFrame(ScrollArea):
    def __init__(
        self,
        title: str,
        title_stylesheet: str = "font-size: 18px; font-weight: bold;",
        spacing: tuple[int, int] = (5, 10),
        margins: tuple[int, int, int, int] = (10, 10, 10, 10),
    ) -> None:
        super().__init__()
        self.confirm_btn = PushButton()

        title_layout = QHBoxLayout()
        title_layout.setSpacing(0)
        title_layout.setContentsMargins(0, 0, 0, 0)

        title_layout.addStretch()
        title_layout.addWidget(Label(text=title, stylesheet=title_stylesheet))
        title_layout.addStretch()

        self._layout = QFormLayout()
        self._layout.setHorizontalSpacing(spacing[0])
        self._layout.setVerticalSpacing(spacing[1])
        self._layout.setContentsMargins(*margins)
        self._layout.addRow(title_layout)

        frame = QFrame()
        frame.setLayout(self._layout)

        self.setWidget(frame)

        self.confirm_btn.clicked.connect(self.on_confirm_clicked)

    def addRow(self, label: str | QWidget, widget: QWidget | QLayout) -> None:
        self._layout.addRow(label, widget)

    def addConfirmButton(self, text: str) -> None:
        self.confirm_btn.setText(text)

        confirm_layout = QHBoxLayout()
        confirm_layout.setSpacing(0)
        confirm_layout.setContentsMargins(0, 0, 0, 0)
        confirm_layout.addStretch()
        confirm_layout.addWidget(self.confirm_btn)
        self._layout.addRow(confirm_layout)

    def on_confirm_clicked(self) -> None:
        raise NotImplementedError("Subclasses must implement this method.")


__all__ = [
    "FormFrame",
]
