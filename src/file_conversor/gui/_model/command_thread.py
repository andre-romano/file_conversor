# src/file_conversor/gui/_model/command_task.py

from typing import override

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QMessageBox

from file_conversor.config import Log, get_translation
from file_conversor.utils.protocols import CommandProtocol


LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class _CommandThread(QThread):
    progress_updated = Signal(float)
    error = Signal(str)

    def __init__(self, command: CommandProtocol) -> None:
        super().__init__()
        self.command = command
        self.command.set_progress_callback(self.progress_updated.emit)

    @override
    def run(self) -> None:
        try:
            self.command.execute()
        except (SystemExit, KeyboardInterrupt):
            logger.warning(f"CommandThread interrupted by user.")
        except Exception as e:
            logger.error(f"CommandThread - {e}")
            self.error.emit(str(e))


class CommandThreadHandler(QObject):
    progress_updated = Signal(float)
    finished = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.__cmd_thread: _CommandThread | None = None
        self.error_msg: str = ""

    def _cleanup_thread(self) -> None:
        if self.__cmd_thread is not None:
            self.__cmd_thread.deleteLater()
            self.__cmd_thread = None
            logger.debug("Command thread cleaned up.")

    def _handle_error(self, msg: str) -> None:
        self.error_msg = msg
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(_("Error"))
        msg_box.setText(msg)  # show the error message as the main text in the popup
        msg_box.exec()  # show the popup

    def start(self, command: CommandProtocol) -> None:
        if self.__cmd_thread is not None and self.__cmd_thread.isRunning():
            raise RuntimeError(_("CommandThreadHandler is already running."))

        self.error_msg = ""
        self.__cmd_thread = _CommandThread(command=command)

        self.__cmd_thread.progress_updated.connect(self.progress_updated.emit)
        self.__cmd_thread.finished.connect(self.finished.emit)
        self.__cmd_thread.finished.connect(self._cleanup_thread)
        self.__cmd_thread.error.connect(self._handle_error)
        self.__cmd_thread.start()


__all__ = [
    "CommandThreadHandler",
]
