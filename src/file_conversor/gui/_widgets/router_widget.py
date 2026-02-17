# src/file_conversor/gui/_widgets/router_widget.py


from PySide6.QtWidgets import QAbstractButton, QStackedWidget, QWidget


class RouterWidget(QStackedWidget):
    def __init__(self, pages: list[tuple[QWidget, QAbstractButton]]) -> None:
        super().__init__()

        def on_click(i: int, btn: QAbstractButton) -> None:
            self.setCurrentIndex(i)
            for _, button in pages:
                button.setChecked(button is btn)

        # Add pages to the stack (Index 0 is Home, Index 1 is Settings)
        for idx, (page, button) in enumerate(pages):
            # add page to stack and connect button to show the page when clicked
            self.addWidget(page)
            button.clicked.connect(lambda _checked=False, i=idx, btn=button: on_click(i, btn))


__all__ = [
    "RouterWidget",
]
