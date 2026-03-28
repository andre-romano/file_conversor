# src/file_conversor/gui/_widgets/input_files.py

from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QFrame, QHBoxLayout, QVBoxLayout

from file_conversor.config import get_translation
from file_conversor.gui._model import FileFilters
from file_conversor.gui._utils import get_qt_icon
from file_conversor.gui._widgets.button import PushButton
from file_conversor.gui._widgets.drag_drop_list import DragDropListWidget


_ = get_translation()


class InputFilesWidget(QFrame):
    def __init__(
        self,
        gui_path: Path,
        spacing: int = 5,
        file_filters: FileFilters | None = None,
        btn_size: tuple[int, int] = (24, 24),
        btn_icon_size: tuple[int, int] = (18, 18),
    ) -> None:
        super().__init__()

        self._file_filters = file_filters if file_filters else FileFilters()

        self._list_widget = DragDropListWidget(
            gui_path=gui_path,
            tooltip=_("List of input files (drag and drop supported)"),
            file_filters=self._file_filters,
        )

        self._open_dialog_btn = PushButton(
            btn_size=btn_size,
            icon=(get_qt_icon("folder-open-outline"), *btn_icon_size),
            tooltip=_("Select input files"),
        )
        self._move_up_btn = PushButton(
            btn_size=btn_size,
            icon=(get_qt_icon("arrow-up-bold"), *btn_icon_size),
            tooltip=_("Move selected files up"),
        )
        self._move_down_btn = PushButton(
            btn_size=btn_size,
            icon=(get_qt_icon("arrow-down-bold"), *btn_icon_size),
            tooltip=_("Move selected files down"),
        )
        self._remove_btn = PushButton(
            btn_size=btn_size,
            icon=(get_qt_icon("delete"), *btn_icon_size),
            tooltip=_("Remove selected files"),
        )

        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(spacing)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addWidget(self._open_dialog_btn)
        btn_layout.addWidget(self._move_up_btn)
        btn_layout.addWidget(self._move_down_btn)
        btn_layout.addWidget(self._remove_btn)
        btn_layout.addStretch()

        layout = QHBoxLayout()
        layout.setSpacing(spacing)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._list_widget, stretch=1)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self._open_dialog_btn.clicked.connect(self._open_file_dialog)
        self._move_up_btn.clicked.connect(self._move_selected_items_up)
        self._move_down_btn.clicked.connect(self._move_selected_items_down)
        self._remove_btn.clicked.connect(self._remove_selected_items)

    def _open_file_dialog(self):
        file_path, _filters = QFileDialog.getOpenFileNames(
            parent=self,
            caption=_("Select input files"),
            dir="",  # Starting directory (empty means current or last used)
            filter=self._file_filters.get(),
        )
        self._list_widget.addItems(file_path)

    def _move_selected_items_up(self):
        sorted_selected = sorted(idx.row() for idx in self._list_widget.selectedIndexes())
        if sorted_selected and sorted_selected[0] > 0:
            for index in sorted_selected:
                item = self._list_widget.takeItem(index)
                self._list_widget.insertItem(index - 1, item)
                item.setSelected(True)

    def _move_selected_items_down(self):
        reversed_selected = sorted((idx.row() for idx in self._list_widget.selectedIndexes()), reverse=True)
        if reversed_selected and reversed_selected[0] < self._list_widget.count() - 1:
            for index in reversed_selected:
                item = self._list_widget.takeItem(index)
                self._list_widget.insertItem(index + 1, item)
                item.setSelected(True)

    def _remove_selected_items(self):
        for index in self._list_widget.selectedIndexes():
            self._list_widget.takeItem(index.row())


__all__ = [
    "InputFilesWidget",
]
