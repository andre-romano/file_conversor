# src/file_conversor/gui/doc/__init__.py

from PySide6.QtWidgets import QPushButton

from file_conversor.gui._widgets.flow_frame import FlowFrame


class DocFrame(FlowFrame):
    def __init__(self) -> None:
        super().__init__()

        # TODO replace test code with real code
        for i in range(15):
            card = QPushButton(f"Card {i + 1}")
            card.setFixedSize(150, 120)  # Give the cards a standard size
            self.addWidget(card)


__all__ = [
    "DocFrame",
]
