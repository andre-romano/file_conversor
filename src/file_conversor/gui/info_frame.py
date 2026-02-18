# src/file_conversor/gui/info_frame.py

from typing import override

from PySide6.QtWidgets import QFrame, QLayout, QVBoxLayout

# CORE
from file_conversor.config import Environment, get_translation

# GUI
from file_conversor.gui._utils import Stretch, get_hlayout, get_qt_icon
from file_conversor.gui._widgets import Label, LabelImage, LabelUrl
from file_conversor.system import System


_ = get_translation()


class InfoFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()
        logo_path = Environment.get_icons_folder() / "icon.png"
        assert logo_path.exists(), f"Logo file not found at {logo_path}"

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 15, 10, 15)  # margin around the whole layout
        layout.setSpacing(4)  # distance between rows

        layout.addLayout(get_hlayout(
            LabelImage(logo_path, (24, 24)),
            Label(f"{_('File Conversor')}", "font-weight: bold;"),  # title
            Stretch(),
            spacing=5,
        ))
        layout.addWidget(Label(f"{_('A simple file conversion utility.')}", "font-style: italic;"))
        layout.addLayout(get_hlayout(
            LabelImage(get_qt_icon("mdi.copyright"), size=(16, 16)),  # copyright icon
            Label(f"Andre Luiz Romano Madureira"),
            Stretch(),
            spacing=3,
        ))
        layout.addLayout(get_hlayout(
            LabelImage(get_qt_icon("mdi.scale-balance"), size=(16, 16)),  # license icon
            LabelUrl("https://www.apache.org/licenses/LICENSE-2.0", "Apache-2.0 license"),
            Stretch(),
            spacing=3,
        ))
        layout.addLayout(get_hlayout(
            LabelImage(get_qt_icon("mdi.home-circle-outline"), size=(16, 16)),  # home icon
            LabelUrl("https://github.com/andre-romano/file_conversor"),
            Stretch(),
            spacing=3,
        ))
        # TODOz: add donation link
        # layout.addLayout(get_hlayout(
        #     Label(_('Documentation')),
        #     LabelUrl("https://github.com/andre-romano/file_conversor"),
        #     Stretch(),
        #     spacing=3,
        # ))
        # layout.addLayout(get_hlayout(
        #     Label(_('Donate')),
        #     LabelUrl("https://github.com/andre-romano/file_conversor"),
        #     Stretch(),
        #     spacing=3,
        # ))

        layout.addWidget(Label())  # add empty label as spacer

        layout.addWidget(Label(f"{_('Environment:')}", "font-weight: bold;"))
        layout.addWidget(Label(f"{_('Resources Folder')}: {Environment.get_resources_folder()}", word_wrap=True))
        layout.addWidget(Label(f"{_('Data Folder')}: {Environment.get_data_folder()}", word_wrap=True))
        layout.addWidget(Label(f"{_('Platform')}: {System.Platform.get()}"))
        layout.addWidget(Label(f"Python {Environment.get_python_version()}"))

        layout.addStretch()  # add stretch at the end of the last row to push content to the top
        self.setLayout(layout)

    @override
    def layout(self) -> QLayout:
        layout = super().layout()
        if layout is None:
            raise RuntimeError("InfoFrame layout is not set")
        return layout


__all__ = [
    "InfoFrame",
]
