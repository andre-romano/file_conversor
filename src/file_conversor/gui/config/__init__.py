# src/file_conversor/gui/config/__init__.py


from PySide6.QtWidgets import QFrame

from file_conversor.config import Environment, get_translation


ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()
_ = get_translation()


class ConfigFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()


__all__ = [
    "ConfigFrame",
]
