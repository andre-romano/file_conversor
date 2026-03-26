# src/file_conversor/gui/_widgets/output_dir.py

from PySide6.QtWidgets import QFileDialog, QFrame, QHBoxLayout, QLineEdit

from file_conversor.config import get_translation
from file_conversor.gui._utils import get_qt_icon
from file_conversor.gui._widgets.button import PushButton


_ = get_translation()


class OutputDirWidget(QFrame):
    def __init__(
        self,
        spacing: int = 5,
    ) -> None:
        super().__init__()

        self.line_edit = QLineEdit()
        self.open_dialog_btn = PushButton(
            btn_size=(24, 24),
            icon=(get_qt_icon("mdi.folder-open-outline"), 18, 18),
            tooltip=_("Select output directory"),
        )

        layout = QHBoxLayout()
        layout.setSpacing(spacing)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.open_dialog_btn)

        self.setLayout(layout)

        self.open_dialog_btn.clicked.connect(self.open_directory_dialog)

    def open_directory_dialog(self):
        file_path = QFileDialog.getExistingDirectory(
            parent=self,
            caption=_("Select output directory"),
            dir="",  # Starting directory (empty means current or last used)
        )
        self.line_edit.setText(file_path)


__all__ = [
    "OutputDirWidget",
]
