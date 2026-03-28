# src/file_conversor/gui/doc/convert.py


from pathlib import Path
from typing import override

from PySide6.QtCore import QThread, Signal

from file_conversor.command.doc import DocConvertCommand
from file_conversor.config import Environment, Log, get_translation
from file_conversor.gui._frames import FormFrame
from file_conversor.gui._model import FileFilter, FileFilters
from file_conversor.gui._utils import configure_qt_window


LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


class _WorkerThread(QThread):
    progress_updated = Signal(float)
    finished = Signal()

    def __init__(self, input_files: list[Path], file_format: str, output_dir: Path) -> None:
        super().__init__()
        self.input_files = input_files
        self.file_format = file_format
        self.output_dir = output_dir

    @override
    def run(self) -> None:
        command = DocConvertCommand()
        command.convert(
            input_files=self.input_files,
            file_format=DocConvertCommand.SupportedOutFormats(self.file_format),
            output_dir=self.output_dir,
            progress_callback=self.progress_updated.emit,
        )
        self.finished.emit()


class DocConvertWindow(FormFrame):
    def __init__(self):
        super().__init__(title=_("Document Convertion"), gui_path=GUI_PATH)
        configure_qt_window(
            self,
            icon_path=ICON_PATH,
            title=_("Document Convertion"),
        )

        self.input_files_widget = self.addInputFiles(FileFilters([
            FileFilter(description=_("Word Documents"), extensions=[mode.value for mode in DocConvertCommand.SupportedInFormats]),
        ]))
        self.output_format_widget = self.addOutputFormat(mode.value for mode in DocConvertCommand.SupportedOutFormats)
        self.output_dir_widget = self.addOutputDirectory()
        self.confirm_btn = self.addConfirmButton()

        self._thread: _WorkerThread | None = None

    @override
    def on_start_btn_clicked(self) -> None:
        logger.debug("Confirm button clicked")
        self.status_bar.startTask(_("Processing files..."), _("Finished!"))
        self.confirm_btn.setEnabled(False)

        self._thread = _WorkerThread(
            input_files=self.input_files_widget.get_files(),
            file_format=self.output_format_widget.get_format(),
            output_dir=self.output_dir_widget.get_directory(),
        )
        self._thread.progress_updated.connect(self.status_bar.setProgress)
        self._thread.finished.connect(self.on_finished_task)
        self._thread.start()

    @override
    def on_finished_task(self) -> None:
        self.status_bar.setProgress(100)
        self.confirm_btn.setEnabled(True)


__all__ = [
    "DocConvertWindow",
]
