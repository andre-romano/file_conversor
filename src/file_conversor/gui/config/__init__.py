# src/file_conversor/gui/config/__init__.py


from PySide6.QtWidgets import QFormLayout, QFrame

from file_conversor.config import Environment, Log, get_translation
from file_conversor.gui._widgets import ScrollArea


LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


class ConfigFrame(ScrollArea):
    def __init__(self) -> None:
        super().__init__()

        layout = QFormLayout()

        frame = QFrame()
        frame.setLayout(layout)

        self.setWidget(frame)


__all__ = [
    "ConfigFrame",
]
