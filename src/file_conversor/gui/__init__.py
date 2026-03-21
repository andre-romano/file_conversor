# src/file_conversor/gui/__init__.py


from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QMainWindow,
)

# CORE
from file_conversor.config import Environment, get_translation

# GUI
from file_conversor.gui._widgets import (
    HLineFrame,
    SidebarFrame,
    StackedRouter,
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


ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()
_ = get_translation()


class MainWindowGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        icon_path = ICON_PATH / "icon.png"
        assert icon_path.exists(), f"{_('App icon file not found:')} {icon_path}"

        self.setWindowTitle(f"File Conversor v{Environment.get_app_version()}")
        self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(800, 540)

        # Sidebar
        icon_size = (28, 28)  # px
        btn_size = (45, 45)  # px

        sidebar = SidebarFrame(gui_path=GUI_PATH)
        sidebar.addItems(
            btn_doc := ToolButton(icon=(ICON_PATH / "docx.ico", *icon_size), tooltip=_("Word tools"), btn_size=btn_size),
            btn_xls := ToolButton(icon=(ICON_PATH / "xls.ico", *icon_size), tooltip=_("Excel tools"), btn_size=btn_size),
            btn_ppt := ToolButton(icon=(ICON_PATH / "ppt.ico", *icon_size), tooltip=_("PowerPoint tools"), btn_size=btn_size),
            HLineFrame(shadow=HLineFrame.Shadow.Sunken),  # separator
            btn_audio := ToolButton(icon=(ICON_PATH / "mp3.ico", *icon_size), tooltip=_("Audio tools"), btn_size=btn_size),
            btn_video := ToolButton(icon=(ICON_PATH / "mp4.ico", *icon_size), tooltip=_("Video tools"), btn_size=btn_size),
            btn_image := ToolButton(icon=(ICON_PATH / "jpg.ico", *icon_size), tooltip=_("Image tools"), btn_size=btn_size),
            HLineFrame(shadow=HLineFrame.Shadow.Sunken),  # separator
            btn_pdf := ToolButton(icon=(ICON_PATH / "pdf.ico", *icon_size), tooltip=_("PDF tools"), btn_size=btn_size),
            btn_ebook := ToolButton(icon=(ICON_PATH / "epub.ico", *icon_size), tooltip=_("Ebook tools"), btn_size=btn_size),
            btn_text := ToolButton(icon=(ICON_PATH / "json.ico", *icon_size), tooltip=_("Text tools"), btn_size=btn_size),
            btn_hash := ToolButton(icon=(ICON_PATH / "sha256.ico", *icon_size), tooltip=_("Hash tools"), btn_size=btn_size),
            sidebar.getStretch(),
            btn_info := ToolButton(icon=(ICON_PATH / "info.ico", *icon_size), tooltip=_("Info"), btn_size=btn_size),
            btn_config := ToolButton(icon=(ICON_PATH / "repair.ico", *icon_size), tooltip=_("Settings"), btn_size=btn_size),
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


__all__ = [
    "MainWindowGUI",
]
