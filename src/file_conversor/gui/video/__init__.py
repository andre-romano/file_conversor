# src/file_conversor/gui/video/__init__.py

from PySide6.QtWidgets import QFrame

from file_conversor.config import Environment, Log, get_translation
from file_conversor.gui._layouts import FlowLayout
from file_conversor.gui._widgets import Card, ScrollArea


LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


class VideoFrame(ScrollArea):
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
            enhance_card := Card(
                icon=ICON_PATH / "color.ico",
                title=_("Enhance"),
                description=_("Enhance the video."),
                gui_path=GUI_PATH,
            ),
            mirror_card := Card(
                icon=ICON_PATH / "left_right.ico",
                title=_("Mirror"),
                description=_("Mirror the video."),
                gui_path=GUI_PATH,
            ),
            rotate_card := Card(
                icon=ICON_PATH / "rotate_right.ico",
                title=_("Rotate"),
                description=_("Rotate the video."),
                gui_path=GUI_PATH,
            ),
            resize_card := Card(
                icon=ICON_PATH / "resize.ico",
                title=_("Resize"),
                description=_("Resize the video."),
                gui_path=GUI_PATH,
            ),
            check_card := Card(
                icon=ICON_PATH / "check.ico",
                title=_("Check"),
                description=_("Check the file."),
                gui_path=GUI_PATH,
            ),
            info_card := Card(
                icon=ICON_PATH / "info.ico",
                title=_("Info"),
                description=_("Information about the file."),
                gui_path=GUI_PATH,
            ),
            list_formats_card := Card(
                icon=ICON_PATH / "mp4.ico",
                title=_("List Formats"),
                description=_("List supported formats."),
                gui_path=GUI_PATH,
            ),
        )

        frame = QFrame()
        frame.setLayout(layout)

        self.setWidget(frame)

        convert_card.clicked.connect(self.on_convert_card_clicked)
        compress_card.clicked.connect(self.on_compress_card_clicked)
        enhance_card.clicked.connect(self.on_enhance_card_clicked)
        mirror_card.clicked.connect(self.on_mirror_card_clicked)
        rotate_card.clicked.connect(self.on_rotate_card_clicked)
        resize_card.clicked.connect(self.on_resize_card_clicked)
        check_card.clicked.connect(self.on_check_card_clicked)
        info_card.clicked.connect(self.on_info_card_clicked)
        list_formats_card.clicked.connect(self.on_list_formats_card_clicked)

    def on_convert_card_clicked(self) -> None:
        logger.debug("Convert card clicked!")

    def on_compress_card_clicked(self) -> None:
        logger.debug("Compress card clicked!")

    def on_enhance_card_clicked(self) -> None:
        logger.debug("Enhance card clicked!")

    def on_mirror_card_clicked(self) -> None:
        logger.debug("Mirror card clicked!")

    def on_rotate_card_clicked(self) -> None:
        logger.debug("Rotate card clicked!")

    def on_resize_card_clicked(self) -> None:
        logger.debug("Resize card clicked!")

    def on_check_card_clicked(self) -> None:
        logger.debug("Check card clicked!")

    def on_info_card_clicked(self) -> None:
        logger.debug("Info card clicked!")

    def on_list_formats_card_clicked(self) -> None:
        logger.debug("List Formats card clicked!")


__all__ = [
    "VideoFrame",
]
