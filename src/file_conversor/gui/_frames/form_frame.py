# src/file_conversor/gui/_widgets/form_frame.py

from pathlib import Path
from typing import Iterable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLayout,
    QVBoxLayout,
    QWidget,
)

from file_conversor.config import get_translation
from file_conversor.gui._frames.statusbar_frame import StatusBarFrame
from file_conversor.gui._model import FileFilters
from file_conversor.gui._widgets import (
    InputFilesWidget,
    Label,
    OutputDirWidget,
    OutputFormatWidget,
    PushButton,
    ScrollArea,
)


_ = get_translation()


class FormFrame(QFrame):
    def __init__(
        self,
        gui_path: Path,
        title: str,
        title_stylesheet: str = "font-size: 18px; font-weight: bold;",
        spacing: tuple[int, int] = (5, 10),
        margins: tuple[int, int, int, int] = (10, 10, 10, 10),
    ) -> None:
        super().__init__()
        self._gui_path = gui_path

        title_label = Label(text=title, stylesheet=title_stylesheet)

        self._form_layout = QFormLayout()
        self._form_layout.setHorizontalSpacing(spacing[0])
        self._form_layout.setVerticalSpacing(spacing[1])
        self._form_layout.setContentsMargins(0, 0, 0, 0)

        form_frame = QFrame()
        form_frame.setLayout(self._form_layout)

        scrollarea = ScrollArea()
        scrollarea.setWidget(form_frame)

        self.status_bar = StatusBarFrame(gui_path=gui_path)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(spacing[1])
        content_layout.setContentsMargins(*margins)
        content_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        content_layout.addWidget(scrollarea, stretch=1)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addLayout(content_layout, stretch=1)
        layout.addWidget(self.status_bar)

        self.setLayout(layout)

        self.status_bar.showMessage(_("Ready!"))

    def addRow(self, label: str | QWidget, widget: QWidget | QLayout) -> None:
        self._form_layout.addRow(label, widget)

    def addInputFiles(self, file_filters: FileFilters | None = None):
        input_files_widget = InputFilesWidget(
            gui_path=self._gui_path,
            file_filters=file_filters,
        )
        self.addRow(f"{_('Input Files')}:", input_files_widget)
        return input_files_widget

    def addOutputFormat(self, extensions: Iterable[str]):
        output_format_widget = OutputFormatWidget(extensions)
        self.addRow(f"{_('Output Format')}:", output_format_widget)
        return output_format_widget

    def addOutputDirectory(self):
        output_dir_widget = OutputDirWidget()
        self.addRow(f"{_('Output directory')}:", output_dir_widget)
        return output_dir_widget

    def addConfirmButton(self):
        confirm_btn = PushButton(text=_("Start"))
        confirm_btn.clicked.connect(self.on_start_btn_clicked)

        confirm_layout = QHBoxLayout()
        confirm_layout.setSpacing(0)
        confirm_layout.setContentsMargins(0, 0, 0, 0)
        confirm_layout.addStretch()
        confirm_layout.addWidget(confirm_btn)
        self._form_layout.addRow(confirm_layout)
        return confirm_btn

    def on_start_btn_clicked(self) -> None:
        raise NotImplementedError("Subclasses must implement this method.")

    def on_finished_task(self) -> None:
        raise NotImplementedError("Subclasses must implement this method.")


__all__ = [
    "FormFrame",
]
