# src/file_conversor/gui/_widgets/output_file.py

from PySide6.QtWidgets import QFileDialog, QFrame, QHBoxLayout, QLineEdit

from file_conversor.config import get_translation
from file_conversor.gui._utils import get_qt_icon
from file_conversor.gui._widgets.button import PushButton


_ = get_translation()


class OutputFileWidget(QFrame):
    def __init__(
        self,
        spacing: int = 5,
    ) -> None:
        super().__init__()

        self.line_edit = QLineEdit()
        self.open_dialog_btn = PushButton(
            btn_size=(24, 24),
            icon=(get_qt_icon("mdi.folder-open-outline"), 18, 18),
            tooltip=_("Select output file"),
        )

        layout = QHBoxLayout()
        layout.setSpacing(spacing)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.open_dialog_btn)

        self.setLayout(layout)

        self.open_dialog_btn.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self, file_filter: str = "All Files (*.*)"):
        file_path, _selected_filter = QFileDialog.getSaveFileName(
            parent=self,
            caption=_("Select output file"),
            dir="",  # Starting directory (empty means current or last used)
            filter=file_filter,
        )
        self.line_edit.setText(file_path)


__all__ = [
    "OutputFileWidget",
]
