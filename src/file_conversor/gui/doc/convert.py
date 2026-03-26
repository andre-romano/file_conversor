# src/file_conversor/gui/doc/convert.py


from typing import override

from PySide6.QtWidgets import QLineEdit

from file_conversor.config import Environment, get_translation
from file_conversor.gui._frames import FormFrame
from file_conversor.gui._utils import configure_qt_window


ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()
_ = get_translation()


class DocConvertWindow(FormFrame):
    def __init__(self):
        super().__init__(title=_("Document Convertion"))
        configure_qt_window(
            self,
            icon_path=ICON_PATH,
            title=_("Document Convertion"),
        )

        self.addRow(f"{_('Input Files')}:", QLineEdit())
        self.addRow(f"{_('Format')}:", QLineEdit())
        self.addRow(f"{_('Output directory')}:", QLineEdit())
        self.addConfirmButton(_("Start"))

    @override
    def on_confirm_clicked(self) -> None:
        print("Start button clicked!")


__all__ = [
    "DocConvertWindow",
]
