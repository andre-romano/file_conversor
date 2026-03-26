# src/file_conversor/gui/xls/__init__.py

from PySide6.QtWidgets import QFrame

from file_conversor.config import Environment, get_translation
from file_conversor.gui._layouts import FlowLayout
from file_conversor.gui._widgets import Card, ScrollArea


ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()
_ = get_translation()


class XlsFrame(ScrollArea):
    def __init__(self) -> None:
        super().__init__()

        layout = FlowLayout()
        layout.addItems(
            convert_card := Card(
                icon=ICON_PATH / "convert.ico",
                title=_("Convert"),
                description=_("Convert to other formats."),
                gui_path=GUI_PATH,
            ),
        )

        frame = QFrame()
        frame.setLayout(layout)

        self.setWidget(frame)

        convert_card.clicked.connect(self.on_convert_card_clicked)

    def on_convert_card_clicked(self) -> None:
        print("Convert card clicked!")


__all__ = [
    "XlsFrame",
]
