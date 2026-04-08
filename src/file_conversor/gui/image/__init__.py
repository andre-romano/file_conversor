# src/file_conversor/gui/image/__init__.py


from PySide6.QtWidgets import QFrame

from file_conversor.config import LOG, Environment, get_translation
from file_conversor.gui._layouts import FlowLayout
from file_conversor.gui._widgets import Card, ScrollArea


_ = get_translation()
logger = LOG.getLogger(__name__)

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


class ImageFrame(ScrollArea):
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
            render_card := Card(
                icon=ICON_PATH / "svg.ico",
                title=_("Render"),
                description=_("Render a vector into an image."),
                gui_path=GUI_PATH,
            ),
            to_pdf_card := Card(
                icon=ICON_PATH / "pdf.ico",
                title=_("To PDF"),
                description=_("Convert to PDF."),
                gui_path=GUI_PATH,
            ),
            compress_card := Card(
                icon=ICON_PATH / "compress.ico",
                title=_("Compress"),
                description=_("Compress the image."),
                gui_path=GUI_PATH,
            ),
            mirror_card := Card(
                icon=ICON_PATH / "left_right.ico",
                title=_("Mirror"),
                description=_("Mirror the image."),
                gui_path=GUI_PATH,
            ),
            rotate_card := Card(
                icon=ICON_PATH / "rotate_right.ico",
                title=_("Rotate"),
                description=_("Rotate the image."),
                gui_path=GUI_PATH,
            ),
            resize_card := Card(
                icon=ICON_PATH / "resize.ico",
                title=_("Resize"),
                description=_("Resize the image."),
                gui_path=GUI_PATH,
            ),
            antialias_card := Card(
                icon=ICON_PATH / "diagonal_line.ico",
                title=_("Antialias"),
                description=_("Apply antialiasing to image."),
                gui_path=GUI_PATH,
            ),
            blur_card := Card(
                icon=ICON_PATH / "blur.ico",
                title=_("Blur"),
                description=_("Apply blur effect to image."),
                gui_path=GUI_PATH,
            ),
            enhance_card := Card(
                icon=ICON_PATH / "color.ico",
                title=_("Enhance"),
                description=_("Enhance the image (color, etc)."),
                gui_path=GUI_PATH,
            ),
            filter_card := Card(
                icon=ICON_PATH / "filter.ico",
                title=_("Filter"),
                description=_("Apply filters to the image."),
                gui_path=GUI_PATH,
            ),
            unsharp_card := Card(
                icon=ICON_PATH / "sharpener.ico",
                title=_("Unsharp mask"),
                description=_("Apply unsharp mask to the image."),
                gui_path=GUI_PATH,
            ),
            info_card := Card(
                icon=ICON_PATH / "info.ico",
                title=_("Info"),
                description=_("Information about the image."),
                gui_path=GUI_PATH,
            ),
        )

        frame = QFrame()
        frame.setLayout(layout)

        self.setWidget(frame)

        convert_card.clicked.connect(self.on_convert_card_clicked)
        render_card.clicked.connect(self.on_render_card_clicked)
        to_pdf_card.clicked.connect(self.on_to_pdf_card_clicked)
        compress_card.clicked.connect(self.on_compress_card_clicked)
        mirror_card.clicked.connect(self.on_mirror_card_clicked)
        rotate_card.clicked.connect(self.on_rotate_card_clicked)
        resize_card.clicked.connect(self.on_resize_card_clicked)
        antialias_card.clicked.connect(self.on_antialias_card_clicked)
        blur_card.clicked.connect(self.on_blur_card_clicked)
        enhance_card.clicked.connect(self.on_enhance_card_clicked)
        filter_card.clicked.connect(self.on_filter_card_clicked)
        unsharp_card.clicked.connect(self.on_unsharp_card_clicked)
        info_card.clicked.connect(self.on_info_card_clicked)

    def on_convert_card_clicked(self) -> None:
        logger.debug("Convert card clicked!")

    def on_render_card_clicked(self) -> None:
        logger.debug("Render card clicked!")

    def on_to_pdf_card_clicked(self) -> None:
        logger.debug("To PDF card clicked!")

    def on_compress_card_clicked(self) -> None:
        logger.debug("Compress card clicked!")

    def on_mirror_card_clicked(self) -> None:
        logger.debug("Mirror card clicked!")

    def on_rotate_card_clicked(self) -> None:
        logger.debug("Rotate card clicked!")

    def on_resize_card_clicked(self) -> None:
        logger.debug("Resize card clicked!")

    def on_antialias_card_clicked(self) -> None:
        logger.debug("Antialias card clicked!")

    def on_blur_card_clicked(self) -> None:
        logger.debug("Blur card clicked!")

    def on_enhance_card_clicked(self) -> None:
        logger.debug("Enhance card clicked!")

    def on_filter_card_clicked(self) -> None:
        logger.debug("Filter card clicked!")

    def on_unsharp_card_clicked(self) -> None:
        logger.debug("Unsharp mask card clicked!")

    def on_info_card_clicked(self) -> None:
        logger.debug("Info card clicked!")


__all__ = [
    "ImageFrame",
]
