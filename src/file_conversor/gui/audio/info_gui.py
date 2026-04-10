# src/file_conversor/gui/audio/info_gui.py


from typing import override

from file_conversor.command.audio import AudioInfoCommand
from file_conversor.command.video.info_cmd import (
    VideoInfoMarkdownStrategy,
)
from file_conversor.config import LOG, Environment, get_translation
from file_conversor.gui._frames import FormFrame
from file_conversor.gui._model import FileFilter, FileFilters
from file_conversor.gui._utils import configure_qt_window


_ = get_translation()
logger = LOG.getLogger(__name__)

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


class AudioInfoWindow(FormFrame):
    def __init__(self):
        super().__init__(title=_("Audio Information"), gui_path=GUI_PATH)
        configure_qt_window(
            self,
            icon_path=ICON_PATH,
            title=_("Audio Information"),
        )

        self._current_command: AudioInfoCommand | None = None
        self.input_files_widget = self.addInputFiles(FileFilters([
            FileFilter(description=_("Audio files"), extensions=AudioInfoCommand.get_in_formats()),
        ]))
        self.output_info_widget = self.addOutputInfo()
        # xTODO add output readonly text area to show the information of the file

    @override
    def on_start_btn_clicked(self) -> None:
        super().on_start_btn_clicked()
        logger.debug("Confirm button clicked")

        self._current_command = AudioInfoCommand(
            input_files=self.input_files_widget.get_files(),
        )
        self.cmd_thread_handler.start(
            command=self._current_command,
        )

    @override
    def on_error_task(self) -> None:
        super().on_error_task()
        self.output_info_widget.setMarkdown(f"**{_('Error:')}**\n{self.err_msg}")

    @override
    def on_sucessful_task(self) -> None:
        super().on_sucessful_task()
        assert self._current_command is not None, "Current command should not be None on successful task completion"
        logger.debug(f"Output: {self._current_command.output}")
        output_strategy = VideoInfoMarkdownStrategy(output=self._current_command.output)
        self.output_info_widget.setMarkdown(output_strategy.get_output_markdown())


__all__ = [
    "AudioInfoWindow",
]
