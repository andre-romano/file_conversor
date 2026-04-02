# src/file_conversor/gui/_widgets/form_frame.py

from pathlib import Path
from typing import Iterable, final

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLayout,
    QVBoxLayout,
    QWidget,
)

# CORE
from file_conversor.config import get_translation

# GUI
from file_conversor.gui._frames.statusbar_frame import StatusBarFrame
from file_conversor.gui._model import CommandThreadHandler, FileFilters
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

        self._start_btn = PushButton(text=_("Start"))
        self._start_btn.clicked.connect(self.on_start_btn_clicked)

        self.status_bar = StatusBarFrame(gui_path=gui_path)

        start_btn_layout = QHBoxLayout()
        start_btn_layout.setSpacing(0)
        start_btn_layout.setContentsMargins(0, 0, 0, 0)
        start_btn_layout.addStretch()
        start_btn_layout.addWidget(self._start_btn)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(spacing[1])
        content_layout.setContentsMargins(*margins)
        content_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        content_layout.addLayout(self._form_layout, stretch=1)
        content_layout.addLayout(start_btn_layout)

        form_frame = QFrame()
        form_frame.setLayout(content_layout)

        scrollarea = ScrollArea()
        scrollarea.setWidget(form_frame)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(scrollarea, stretch=1)
        layout.addWidget(self.status_bar)

        self.setLayout(layout)

        self.status_bar.showMessage(_("Ready!"))

        self.cmd_thread_handler = CommandThreadHandler()
        self.cmd_thread_handler.progress_updated.connect(self.status_bar.setProgress)
        self.cmd_thread_handler.finished.connect(self._on_finished_task)

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

    def on_start_btn_clicked(self) -> None:
        """ Override this method to implement the logic when the start button is clicked."""
        self._start_btn.setEnabled(False)
        self.status_bar.startTask(_("Processing files..."), _("Finished!"))

    @final
    def _on_finished_task(self) -> None:
        self._start_btn.setEnabled(True)
        if self.cmd_thread_handler.error_msg:
            self.on_error_task()
        else:
            self.on_sucessful_task()

    def on_error_task(self) -> None:
        msg = self.cmd_thread_handler.error_msg
        self.status_bar.showMessage(f"{_('Error:')} {msg}")

    def on_sucessful_task(self) -> None:
        self.status_bar.setProgress(100)


__all__ = [
    "FormFrame",
]
