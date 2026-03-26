# src/file_conversor/gui/_widgets/form_confirm_btn.py

from PySide6.QtWidgets import QFrame, QHBoxLayout

from file_conversor.gui._widgets.button import PushButton


class FormConfirmFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.confirm_btn = PushButton(text="Start")

        confirm_layout = QHBoxLayout()
        confirm_layout.setSpacing(0)
        confirm_layout.setContentsMargins(0, 0, 0, 0)
        confirm_layout.addStretch()
        confirm_layout.addWidget(self.confirm_btn)

        self.setLayout(confirm_layout)


__all__ = [
    "FormConfirmFrame",
]
