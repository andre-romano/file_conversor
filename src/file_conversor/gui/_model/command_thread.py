# src/file_conversor/gui/_model/command_task.py

from typing import override

from PySide6.QtCore import QThread, Signal

from file_conversor.utils.protocols import CommandProtocol


class CommandThread(QThread):
    progress_updated = Signal(float)
    finished = Signal()

    def __init__(self, command: CommandProtocol) -> None:
        super().__init__()
        self.command = command
        self.command.set_progress_callback(self.progress_updated.emit)

    @override
    def run(self) -> None:
        self.command.execute()
        self.finished.emit()


__all__ = [
    "CommandThread",
]
