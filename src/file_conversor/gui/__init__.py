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
    RouterWidget,
    SidebarButton,
    SidebarFrame,
)
from file_conversor.gui.audio import AudioFrame
from file_conversor.gui.config import ConfigFrame
from file_conversor.gui.doc import DocFrame
from file_conversor.gui.ebook import EbookFrame
from file_conversor.gui.hash import HashFrame
from file_conversor.gui.image import ImageFrame
from file_conversor.gui.pdf import PdfFrame
from file_conversor.gui.ppt import PptFrame
from file_conversor.gui.text import TextFrame
from file_conversor.gui.video import VideoFrame
from file_conversor.gui.xls import XlsFrame


ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()
_ = get_translation()


class MainSidebarButton(SidebarButton):
    def __init__(self, tooltip: str, icon_file: str, icon_width: int, btn_width: int) -> None:
        super().__init__(
            tooltip=tooltip,
            icon_file=ICON_PATH / icon_file,
            icon_width=icon_width,
            icon_height=icon_width,
            btn_width=btn_width,
            btn_height=btn_width,
        )


class MainSidebarFrame(SidebarFrame):
    def __init__(self) -> None:
        icon_width = 28  # px
        btn_width = 45  # px

        super().__init__(
            gui_path=GUI_PATH,
            width=btn_width,
        )

        self.btn_doc = MainSidebarButton(icon_file="docx.ico", tooltip=_("Word tools"), btn_width=btn_width, icon_width=icon_width)
        self.btn_xls = MainSidebarButton(icon_file="xls.ico", tooltip=_("Excel tools"), btn_width=btn_width, icon_width=icon_width)
        self.btn_ppt = MainSidebarButton(icon_file="ppt.ico", tooltip=_("PowerPoint tools"), btn_width=btn_width, icon_width=icon_width)

        self.btn_audio = MainSidebarButton(icon_file="mp3.ico", tooltip=_("Audio tools"), btn_width=btn_width, icon_width=icon_width)
        self.btn_video = MainSidebarButton(icon_file="mp4.ico", tooltip=_("Video tools"), btn_width=btn_width, icon_width=icon_width)
        self.btn_image = MainSidebarButton(icon_file="jpg.ico", tooltip=_("Image tools"), btn_width=btn_width, icon_width=icon_width)

        self.btn_pdf = MainSidebarButton(icon_file="pdf.ico", tooltip=_("PDF tools"), btn_width=btn_width, icon_width=icon_width)
        self.btn_ebook = MainSidebarButton(icon_file="epub.ico", tooltip=_("Ebook tools"), btn_width=btn_width, icon_width=icon_width)
        self.btn_text = MainSidebarButton(icon_file="json.ico", tooltip=_("Text tools"), btn_width=btn_width, icon_width=icon_width)
        self.btn_hash = MainSidebarButton(icon_file="sha256.ico", tooltip=_("Hash tools"), btn_width=btn_width, icon_width=icon_width)

        self.btn_config = MainSidebarButton(icon_file="repair.ico", tooltip=_("Settings"), btn_width=btn_width, icon_width=icon_width)

        self.layout().addWidget(self.btn_doc)
        self.layout().addWidget(self.btn_xls)
        self.layout().addWidget(self.btn_ppt)
        self.layout().addWidget(HLineFrame(shadow=HLineFrame.Shadow.Sunken))  # separator
        self.layout().addWidget(self.btn_audio)
        self.layout().addWidget(self.btn_video)
        self.layout().addWidget(self.btn_image)
        self.layout().addWidget(HLineFrame(shadow=HLineFrame.Shadow.Sunken))  # separator
        self.layout().addWidget(self.btn_pdf)
        self.layout().addWidget(self.btn_ebook)
        self.layout().addWidget(self.btn_text)
        self.layout().addWidget(self.btn_hash)
        self.layout().addStretch()
        self.layout().addWidget(self.btn_config)


class MainWindowGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        icon_path = ICON_PATH / "icon.png"
        assert icon_path.exists(), f"{_('App icon file not found:')} {icon_path}"

        qss_path = GUI_PATH / "main.qss"
        assert qss_path.exists(), f"{_('App main QSS file not found:')} {qss_path}"

        self.setWindowTitle(f"File Conversor v{Environment.get_app_version()}")
        self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(800, 540)

        # Sidebar, and Router
        sidebar_widget = MainSidebarFrame()
        stacked_widget = RouterWidget([
            (DocFrame(), sidebar_widget.btn_doc),
            (XlsFrame(), sidebar_widget.btn_xls),
            (PptFrame(), sidebar_widget.btn_ppt),
            (AudioFrame(), sidebar_widget.btn_audio),
            (VideoFrame(), sidebar_widget.btn_video),
            (ImageFrame(), sidebar_widget.btn_image),
            (PdfFrame(), sidebar_widget.btn_pdf),
            (EbookFrame(), sidebar_widget.btn_ebook),
            (TextFrame(), sidebar_widget.btn_text),
            (HashFrame(), sidebar_widget.btn_hash),
            (ConfigFrame(), sidebar_widget.btn_config),
        ])

        # Layout (Row direction)
        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(stacked_widget, stretch=1)  # The router takes up remaining space
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Central Widget
        central_widget = QFrame()
        central_widget.setObjectName("main")
        central_widget.setStyleSheet(qss_path.read_text())
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


__all__ = [
    "MainWindowGUI",
]
