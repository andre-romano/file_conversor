# src/file_conversor/gui/__init__.py


from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QMainWindow,
)

from file_conversor.config import LOG, Environment, get_translation
from file_conversor.gui._frames import (
    SidebarFrame,
    StackedRouter,
)
from file_conversor.gui._utils import configure_qt_window
from file_conversor.gui._widgets import (
    HLineFrame,
    ToolButton,
)
from file_conversor.gui.audio import AudioFrame
from file_conversor.gui.config import ConfigFrame
from file_conversor.gui.doc import DocFrame
from file_conversor.gui.ebook import EbookFrame
from file_conversor.gui.hash import HashFrame
from file_conversor.gui.image import ImageFrame
from file_conversor.gui.info_frame import InfoFrame
from file_conversor.gui.pdf import PdfFrame
from file_conversor.gui.ppt import PptFrame
from file_conversor.gui.text import TextFrame
from file_conversor.gui.video import VideoFrame
from file_conversor.gui.xls import XlsFrame


_ = get_translation()
logger = LOG.getLogger(__name__)

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


class MainWindowGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        configure_qt_window(self, icon_path=ICON_PATH, size=(800, 540))

        # Sidebar
        icon_size = (28, 28)  # px
        btn_size = (45, 45)  # px

        sidebar = SidebarFrame(gui_path=GUI_PATH)
        sidebar.addItems(
            btn_doc := ToolButton(icon=(ICON_PATH / "docx.ico", *icon_size), tooltip=_("Word tools"), btn_size=btn_size, checkable=True),
            btn_xls := ToolButton(icon=(ICON_PATH / "xls.ico", *icon_size), tooltip=_("Excel tools"), btn_size=btn_size, checkable=True),
            btn_ppt := ToolButton(icon=(ICON_PATH / "ppt.ico", *icon_size), tooltip=_("PowerPoint tools"), btn_size=btn_size, checkable=True),
            HLineFrame(shadow=HLineFrame.Shadow.Sunken),  # separator
            btn_audio := ToolButton(icon=(ICON_PATH / "mp3.ico", *icon_size), tooltip=_("Audio tools"), btn_size=btn_size, checkable=True),
            btn_video := ToolButton(icon=(ICON_PATH / "mp4.ico", *icon_size), tooltip=_("Video tools"), btn_size=btn_size, checkable=True),
            btn_image := ToolButton(icon=(ICON_PATH / "jpg.ico", *icon_size), tooltip=_("Image tools"), btn_size=btn_size, checkable=True),
            HLineFrame(shadow=HLineFrame.Shadow.Sunken),  # separator
            btn_pdf := ToolButton(icon=(ICON_PATH / "pdf.ico", *icon_size), tooltip=_("PDF tools"), btn_size=btn_size, checkable=True),
            btn_ebook := ToolButton(icon=(ICON_PATH / "epub.ico", *icon_size), tooltip=_("Ebook tools"), btn_size=btn_size, checkable=True),
            btn_text := ToolButton(icon=(ICON_PATH / "json.ico", *icon_size), tooltip=_("Text tools"), btn_size=btn_size, checkable=True),
            btn_hash := ToolButton(icon=(ICON_PATH / "sha256.ico", *icon_size), tooltip=_("Hash tools"), btn_size=btn_size, checkable=True),
            sidebar.getStretch(),
            btn_info := ToolButton(icon=(ICON_PATH / "info.ico", *icon_size), tooltip=_("Info"), btn_size=btn_size, checkable=True),
            btn_config := ToolButton(icon=(ICON_PATH / "repair.ico", *icon_size), tooltip=_("Settings"), btn_size=btn_size, checkable=True),
        )

        # Router
        stacked_router = StackedRouter([
            (DocFrame, btn_doc),
            (XlsFrame, btn_xls),
            (PptFrame, btn_ppt),
            (AudioFrame, btn_audio),
            (VideoFrame, btn_video),
            (ImageFrame, btn_image),
            (PdfFrame, btn_pdf),
            (EbookFrame, btn_ebook),
            (TextFrame, btn_text),
            (HashFrame, btn_hash),
            (InfoFrame, btn_info),
            (ConfigFrame, btn_config),
        ])

        # Layout (Row direction)
        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar)
        main_layout.addWidget(stacked_router, stretch=1)  # The router takes up remaining space
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Central Widget
        central_widget = QFrame()
        central_widget.setObjectName("main_window")
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        logger.debug("MainWindow initialized")


__all__ = [
    "MainWindowGUI",
]
