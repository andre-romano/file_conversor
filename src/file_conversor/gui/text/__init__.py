# src/file_conversor/gui/text/__init__.py


from PySide6.QtWidgets import QFrame

from file_conversor.config import Environment, get_translation
from file_conversor.gui._layouts.flow_layout import FlowLayout
from file_conversor.gui._widgets import Card, ScrollArea


ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()
_ = get_translation()


class TextFrame(ScrollArea):
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
            compress_card := Card(
                icon=ICON_PATH / "compress.ico",
                title=_("Compress"),
                description=_("Compress the file."),
                gui_path=GUI_PATH,
            ),
            check_card := Card(
                icon=ICON_PATH / "check.ico",
                title=_("Check"),
                description=_("Check the file."),
                gui_path=GUI_PATH,
            ),
        )

        frame = QFrame()
        frame.setLayout(layout)

        self.setWidget(frame)

        convert_card.clicked.connect(self.on_convert_card_clicked)
        compress_card.clicked.connect(self.on_compress_card_clicked)
        check_card.clicked.connect(self.on_check_card_clicked)

    def on_convert_card_clicked(self) -> None:
        print("Convert card clicked!")

    def on_compress_card_clicked(self) -> None:
        print("Compress card clicked!")

    def on_check_card_clicked(self) -> None:
        print("Check card clicked!")


__all__ = [
    "TextFrame",
]
