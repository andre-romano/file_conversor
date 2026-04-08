# src/file_conversor/gui/xls/convert.py


from typing import override

from file_conversor.command.xls import XlsConvertCommand, XlsConvertOutFormats
from file_conversor.config import Environment, Log, get_translation
from file_conversor.gui._frames import FormFrame
from file_conversor.gui._model import FileFilter, FileFilters
from file_conversor.gui._utils import configure_qt_window


LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


class XlsConvertWindow(FormFrame):
    def __init__(self):
        super().__init__(title=_("Spreadsheet Convertion"), gui_path=GUI_PATH)
        configure_qt_window(
            self,
            icon_path=ICON_PATH,
            title=_("Spreadsheet Convertion"),
        )

        self.input_files_widget = self.addInputFiles(FileFilters([
            FileFilter(description=_("Spreadsheet files"), extensions=XlsConvertCommand.get_in_formats()),
        ]))
        self.output_format_widget = self.addOutputFormat(XlsConvertCommand.get_out_formats())
        self.output_dir_widget = self.addOutputDirectory()

    @override
    def on_start_btn_clicked(self) -> None:
        super().on_start_btn_clicked()
        logger.debug("Confirm button clicked")

        self.cmd_thread_handler.start(
            command=XlsConvertCommand(
                input_files=self.input_files_widget.get_files(),
                file_format=XlsConvertOutFormats(self.output_format_widget.get_format()),
                output_dir=self.output_dir_widget.get_directory(),
            )
        )


__all__ = [
    "XlsConvertWindow",
]
