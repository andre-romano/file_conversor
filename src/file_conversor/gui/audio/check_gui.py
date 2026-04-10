# src/file_conversor/gui/audio/check_gui.py


from typing import override

from file_conversor.command.audio import AudioCheckCommand
from file_conversor.config import LOG, Environment, get_translation
from file_conversor.gui._frames import FormFrame
from file_conversor.gui._model import FileFilter, FileFilters
from file_conversor.gui._utils import configure_qt_window


_ = get_translation()
logger = LOG.getLogger(__name__)

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


class AudioCheckWindow(FormFrame):
    def __init__(self):
        super().__init__(title=_("Audio Check"), gui_path=GUI_PATH)
        configure_qt_window(
            self,
            icon_path=ICON_PATH,
            title=_("Audio Check"),
        )

        self.input_files_widget = self.addInputFiles(FileFilters([
            FileFilter(description=_("Audio files"), extensions=AudioCheckCommand.get_in_formats()),
        ]))

    @override
    def on_start_btn_clicked(self) -> None:
        super().on_start_btn_clicked()
        logger.debug("Confirm button clicked")

        self.cmd_thread_handler.start(
            command=AudioCheckCommand(
                input_files=self.input_files_widget.get_files(),
            )
        )


__all__ = [
    "AudioCheckWindow",
]
