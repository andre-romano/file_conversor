# src/file_conversor/gui/_widgets/drag_drop_list.py

from pathlib import Path
from typing import override

from natsort import natsorted, ns
from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PySide6.QtWidgets import QListWidget

from file_conversor.config import Log, get_translation
from file_conversor.gui._model.file_filter import FileFilters


LOG = Log.get_instance()
logger = LOG.getLogger(__name__)
_ = get_translation()


class DragDropListWidget(QListWidget):
    SelectionMode = QListWidget.SelectionMode

    def __init__(
        self,
        gui_path: Path,
        tooltip: str = "",
        selection_mode: QListWidget.SelectionMode = SelectionMode.ExtendedSelection,
        file_filters: FileFilters | None = None,
    ):
        super().__init__()
        file_filters = file_filters if file_filters else FileFilters()
        self._file_extensions: list[str] = file_filters.get_extensions()

        qss_stylesheet_file = gui_path / "drag_drop_list.qss"
        assert qss_stylesheet_file.is_file(), f"Stylesheet file not found: {qss_stylesheet_file}"

        self.setStyleSheet(qss_stylesheet_file.read_text(encoding="utf-8"))
        self.setAcceptDrops(True)
        self.setToolTip(tooltip) if tooltip else None
        self.setSelectionMode(selection_mode)

    def _accept_action(self, event: QDropEvent) -> bool:
        # Check if the dragged data contains URLs (files)
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            return True
        event.ignore()
        return False

    # mouse enters the widget while dragging
    @override
    def dragEnterEvent(self, event: QDragEnterEvent):
        self._accept_action(event)

    # mouse is moving around inside the widget
    @override
    def dragMoveEvent(self, event: QDragMoveEvent):
        self._accept_action(event)

    # user lets go of the mouse button
    @override
    def dropEvent(self, event: QDropEvent):
        if not self._accept_action(event):
            return

        # Loop through all the dropped files
        urls = natsorted(
            event.mimeData().urls(),
            key=lambda u: u.toLocalFile(),
            alg=ns.PATH | ns.LOCALE | ns.IGNORECASE,
        )
        for url in urls:
            # Get the actual string path (e.g., "C:/Users/file.pdf")
            file_path = url.toLocalFile()
            ext = Path(file_path).suffix.lower()
            logger.debug(f"Drag drop - File: {file_path}, Extension: {ext}, Allowed: {self._file_extensions}")
            if file_path and (ext in self._file_extensions or ".*" in self._file_extensions):
                self.addItem(file_path)


__all__ = [
    "DragDropListWidget",
]
