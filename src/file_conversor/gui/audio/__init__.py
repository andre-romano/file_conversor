# src/file_conversor/gui/audio/__init__.py

from PySide6.QtWidgets import QFrame

from file_conversor.config import LOG, Environment, get_translation
from file_conversor.gui._layouts import FlowLayout
from file_conversor.gui._model import WindowHandler
from file_conversor.gui._widgets import Card, ScrollArea
from file_conversor.gui.audio.check_gui import AudioCheckWindow
from file_conversor.gui.audio.convert_gui import AudioConvertWindow
from file_conversor.gui.audio.info_gui import AudioInfoWindow


_ = get_translation()
logger = LOG.getLogger(__name__)

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


class AudioFrame(ScrollArea):
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
            info_card := Card(
                icon=ICON_PATH / "info.ico",
                title=_("Info"),
                description=_("Information about the file."),
                gui_path=GUI_PATH,
            ),
            check_card := Card(
                icon=ICON_PATH / "check.ico",
                title=_("Check"),
                description=_("Check the file."),
                gui_path=GUI_PATH,
            ),
        )
        self.window_handler = [
            WindowHandler(
                show_window=convert_card.clicked,
                window_cls=AudioConvertWindow,
            ),
            WindowHandler(
                show_window=info_card.clicked,
                window_cls=AudioInfoWindow,
            ),
            WindowHandler(
                show_window=check_card.clicked,
                window_cls=AudioCheckWindow,
            )
        ]

        frame = QFrame()
        frame.setLayout(layout)

        self.setWidget(frame)


__all__ = [
    "AudioFrame",
]
