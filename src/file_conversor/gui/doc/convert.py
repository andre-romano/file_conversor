# src/file_conversor/gui/doc/convert.py


from typing import override

from file_conversor.command.doc import DocConvertCommand, DocConvertOutFormats
from file_conversor.config import Environment, Log, get_translation
from file_conversor.gui._frames import FormFrame
from file_conversor.gui._model import CommandThread, FileFilter, FileFilters
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

        self.input_files_widget = self.addInputFiles(FileFilters([
            FileFilter(description=_("Word Documents"), extensions=DocConvertCommand.get_in_formats()),
        ]))
        self.output_format_widget = self.addOutputFormat(DocConvertCommand.get_out_formats())
        self.output_dir_widget = self.addOutputDirectory()
        self.cmd_thread: CommandThread | None = None

    @override
    def on_start_btn_clicked(self) -> None:
        super().on_start_btn_clicked()
        logger.debug("Confirm button clicked")
        self.status_bar.startTask(_("Processing files..."), _("Finished!"))

        self.cmd_thread = CommandThread(
            command=DocConvertCommand(
                input_files=self.input_files_widget.get_files(),
                file_format=DocConvertOutFormats(self.output_format_widget.get_format()),
                output_dir=self.output_dir_widget.get_directory(),
            )
        )
        self.cmd_thread.progress_updated.connect(self.status_bar.setProgress)
        self.cmd_thread.finished.connect(self.on_finished_task)
        self.cmd_thread.start()


__all__ = [
    "DocConvertWindow",
]
