# src/file_conversor/gui/pdf/__init__.py

from PySide6.QtWidgets import QFrame

from file_conversor.config import Environment, get_translation
from file_conversor.gui._layouts import FlowLayout
from file_conversor.gui._widgets import Card, ScrollArea


ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()
_ = get_translation()


class PdfFrame(ScrollArea):
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
            extract_img_card := Card(
                icon=ICON_PATH / "separate.ico",
                title=_("Extract Image"),
                description=_("Extract images from the PDF."),
                gui_path=GUI_PATH,
            ),
            repair_card := Card(
                icon=ICON_PATH / "repair.ico",
                title=_("Repair"),
                description=_("Repair the PDF."),
                gui_path=GUI_PATH,
            ),
            compress_card := Card(
                icon=ICON_PATH / "compress.ico",
                title=_("Compress"),
                description=_("Compress the PDF."),
                gui_path=GUI_PATH,
            ),
            extract_card := Card(
                icon=ICON_PATH / "extract.ico",
                title=_("Extract"),
                description=_("Extract pages from PDF."),
                gui_path=GUI_PATH,
            ),
            merge_card := Card(
                icon=ICON_PATH / "merge.ico",
                title=_("Merge"),
                description=_("Merge PDF files."),
                gui_path=GUI_PATH,
            ),
            rotate_card := Card(
                icon=ICON_PATH / "rotate_right.ico",
                title=_("Rotate"),
                description=_("Rotate the PDF."),
                gui_path=GUI_PATH,
            ),
            split_card := Card(
                icon=ICON_PATH / "split.ico",
                title=_("Split"),
                description=_("Split PDF into multiple files."),
                gui_path=GUI_PATH,
            ),
            ocr_card := Card(
                icon=ICON_PATH / "ocr.ico",
                title=_("OCR"),
                description=_("Perform OCR on the PDF."),
                gui_path=GUI_PATH,
            ),
            encrypt_card := Card(
                icon=ICON_PATH / "padlock_locked.ico",
                title=_("Encrypt"),
                description=_("Encrypt the PDF."),
                gui_path=GUI_PATH,
            ),
            decrypt_card := Card(
                icon=ICON_PATH / "padlock_unlocked.ico",
                title=_("Decrypt"),
                description=_("Decrypt the PDF."),
                gui_path=GUI_PATH,
            ),
        )

        frame = QFrame()
        frame.setLayout(layout)

        self.setWidget(frame)

        convert_card.clicked.connect(self.on_convert_card_clicked)
        extract_img_card.clicked.connect(self.on_extract_img_card_clicked)
        repair_card.clicked.connect(self.on_repair_card_clicked)
        compress_card.clicked.connect(self.on_compress_card_clicked)
        extract_card.clicked.connect(self.on_extract_card_clicked)
        merge_card.clicked.connect(self.on_merge_card_clicked)
        rotate_card.clicked.connect(self.on_rotate_card_clicked)
        split_card.clicked.connect(self.on_split_card_clicked)
        ocr_card.clicked.connect(self.on_ocr_card_clicked)
        encrypt_card.clicked.connect(self.on_encrypt_card_clicked)
        decrypt_card.clicked.connect(self.on_decrypt_card_clicked)

    def on_convert_card_clicked(self) -> None:
        print("Convert card clicked!")

    def on_extract_img_card_clicked(self) -> None:
        print("Extract Image card clicked!")

    def on_repair_card_clicked(self) -> None:
        print("Repair card clicked!")

    def on_compress_card_clicked(self) -> None:
        print("Compress card clicked!")

    def on_extract_card_clicked(self) -> None:
        print("Extract card clicked!")

    def on_merge_card_clicked(self) -> None:
        print("Merge card clicked!")

    def on_rotate_card_clicked(self) -> None:
        print("Rotate card clicked!")

    def on_split_card_clicked(self) -> None:
        print("Split card clicked!")

    def on_ocr_card_clicked(self) -> None:
        print("OCR card clicked!")

    def on_encrypt_card_clicked(self) -> None:
        print("Encrypt card clicked!")

    def on_decrypt_card_clicked(self) -> None:
        print("Decrypt card clicked!")


__all__ = [
    "PdfFrame",
]
