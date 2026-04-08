# src/file_conversor/gui/xls/__init__.py

from PySide6.QtWidgets import QFrame

from file_conversor.config import LOG, Environment, get_translation
from file_conversor.gui._layouts import FlowLayout
from file_conversor.gui._model.window_handler import WindowHandler
from file_conversor.gui._widgets import Card, ScrollArea
from file_conversor.gui.xls.convert_gui import XlsConvertWindow


_ = get_translation()
logger = LOG.getLogger(__name__)

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


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
        self.window_handler = [
            WindowHandler(
                show_window=convert_card.clicked,
                window_cls=XlsConvertWindow,
            ),
        ]

        frame = QFrame()
        frame.setLayout(layout)

        self.setWidget(frame)


__all__ = [
    "XlsFrame",
]
