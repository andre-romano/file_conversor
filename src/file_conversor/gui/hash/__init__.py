# src/file_conversor/gui/hash/__init__.py


from PySide6.QtWidgets import QFrame

from file_conversor.config import LOG, Environment, get_translation
from file_conversor.gui._layouts import FlowLayout
from file_conversor.gui._widgets import Card, ScrollArea


_ = get_translation()
logger = LOG.getLogger(__name__)

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


class HashFrame(ScrollArea):
    def __init__(self) -> None:
        super().__init__()

        layout = FlowLayout()
        layout.addItems(
            create_card := Card(
                icon=ICON_PATH / "sha256.ico",
                title=_("Create"),
                description=_("Create a hash (sha256, etc) of files."),
                gui_path=GUI_PATH,
            ),
            check_card := Card(
                icon=ICON_PATH / "check.ico",
                title=_("Check"),
                description=_("Check the hash (sha256, etc) of files."),
                gui_path=GUI_PATH,
            ),
        )

        frame = QFrame()
        frame.setLayout(layout)

        self.setWidget(frame)

        create_card.clicked.connect(self.on_create_card_clicked)
        check_card.clicked.connect(self.on_check_card_clicked)

    def on_create_card_clicked(self) -> None:
        logger.debug("Create card clicked!")

    def on_check_card_clicked(self) -> None:
        logger.debug("Check card clicked!")


__all__ = [
    "HashFrame",
]
