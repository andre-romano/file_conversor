# src/file_conversor/gui/doc/convert.py


from typing import override

from PySide6.QtCore import QTimer

from file_conversor.config import Environment, Log, get_translation
from file_conversor.gui._frames import FormFrame
from file_conversor.gui._utils import configure_qt_window


LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


class DocConvertWindow(FormFrame):
    def __init__(self):
        super().__init__(title=_("Document Convertion"), gui_path=GUI_PATH)
        configure_qt_window(
            self,
            icon_path=ICON_PATH,
            title=_("Document Convertion"),
        )

        self.input_files_widget = self.addInputFiles()
        self.output_format_widget = self.addOutputFormat()
        self.output_dir_widget = self.addOutputDirectory()
        self.confirm_btn = self.addConfirmButton()

    @override
    def on_confirm_clicked(self) -> None:
        logger.debug("Confirm button clicked")
        self.status_bar.startTask(_("Processing files..."), _("Finished!"))
        for i in range(20, 101, 20):
            QTimer().singleShot(2000 * i // 20, lambda i=i: self.status_bar.setProgress(i))  # pyright: ignore[reportUnknownArgumentType]


__all__ = [
    "DocConvertWindow",
]
