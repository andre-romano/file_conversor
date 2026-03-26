# src/file_conversor/gui/_widgets/statusbar.py


from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QProgressBar

from file_conversor.utils import EmaEta


class StatusBarFrame(QFrame):
    finished = Signal()

    def __init__(
            self,
            gui_path: Path,
            spacing: int = 35,
            margins: tuple[int, int, int, int] = (3, 3, 3, 3),
            progress_bar_min_width: int = 160,
            progress_bar_height: int = 16,
    ) -> None:
        super().__init__()
        stylesheet_file = gui_path / "statusbar.qss"
        assert stylesheet_file.exists(), f"'StatusBar stylesheet file not found:' {stylesheet_file}"
        self.setStyleSheet(stylesheet_file.read_text(encoding="utf-8"))

        layout = QHBoxLayout()
        layout.setSpacing(spacing)
        layout.setContentsMargins(*margins)

        self._label_message = QLabel("")
        self._label_eta = QLabel("")

        self._progress_bar = QProgressBar(minimum=0, maximum=100, value=0)
        self._progress_bar.setMinimumWidth(progress_bar_min_width)
        self._progress_bar.setFixedHeight(progress_bar_height)
        self._progress_bar.setVisible(False)

        layout.addWidget(self._label_message, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addStretch()
        layout.addWidget(self._progress_bar, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addStretch()
        layout.addWidget(self._label_eta, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(layout)

        self._eta = EmaEta()

    def setProgress(self, value: int | float):
        value = round(value)
        if value < 0 or value > 100:
            raise ValueError("Progress value must be between 0 and 100.")

        self._progress_bar.setValue(value)
        self._progress_bar.setVisible(True)
        if value == 100:
            self.finished.emit()
        self._label_eta.setText(f"ETA: {self._eta.estimate_eta(value)}")

    def showMessage(self, message: str):
        self._label_message.setText(message)

    def startTask(self, message: str, finished_message: str = ""):
        self._eta = EmaEta()
        self.setProgress(0)
        self.showMessage(message)
        if finished_message:
            self.finished.connect(lambda: self.showMessage(finished_message))


__all__ = [
    "StatusBarFrame",
]
