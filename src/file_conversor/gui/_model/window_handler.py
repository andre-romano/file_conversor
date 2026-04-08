# src/file_conversor/gui/_model/window_handler.py


from PySide6.QtCore import Qt, SignalInstance
from PySide6.QtWidgets import QWidget

# GUI
from file_conversor.config import Environment, Log, get_translation


LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


class WindowHandler:
    def __init__(self, show_window: SignalInstance, window_cls: type[QWidget]) -> None:
        super().__init__()
        self._clicked = show_window
        self._window_cls = window_cls
        self._window: QWidget | None = None

        self._clicked.connect(self._on_window_show)

    def _on_window_show(self) -> None:
        logger.debug(f"Window show event - {self._window_cls.__name__}")
        self._window = self._window_cls() if self._window is None else self._window
        # Monitor destroy event to release window reference memory
        self._window.destroyed.connect(self._on_window_destroyed)
        # Force Qt to delete the C++ object on close
        self._window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self._window.show()

    def _on_window_destroyed(self) -> None:
        logger.debug(f"Window destroyed - {self._window.__class__.__name__}")
        self._window = None


__all__ = [
    "WindowHandler",
]
