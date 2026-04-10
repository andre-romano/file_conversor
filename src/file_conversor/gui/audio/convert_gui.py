# src/file_conversor/gui/audio/convert_gui.py


from typing import override

from file_conversor.command.audio import AudioConvertCommand, AudioConvertOutFormats
from file_conversor.config import LOG, Environment, get_translation
from file_conversor.gui._frames import FormFrame
from file_conversor.gui._model import FileFilter, FileFilters
from file_conversor.gui._utils import configure_qt_window


_ = get_translation()
logger = LOG.getLogger(__name__)

ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()


class AudioConvertWindow(FormFrame):
    def __init__(self):
        super().__init__(title=_("Audio Convertion"), gui_path=GUI_PATH)
        configure_qt_window(
            self,
            icon_path=ICON_PATH,
            title=_("Audio Convertion"),
        )

        self.input_files_widget = self.addInputFiles(FileFilters([
            FileFilter(description=_("Audio files"), extensions=AudioConvertCommand.get_in_formats()),
        ]))
        self.output_format_widget = self.addOutputFormat(AudioConvertCommand.get_out_formats())
        self.audio_bitrate = self.addAudioBitrate()
        self.output_dir_widget = self.addOutputDirectory()

    @override
    def on_start_btn_clicked(self) -> None:
        super().on_start_btn_clicked()
        logger.debug("Confirm button clicked")

        self.cmd_thread_handler.start(
            command=AudioConvertCommand(
                input_files=self.input_files_widget.get_files(),
                file_format=AudioConvertOutFormats(self.output_format_widget.get_format()),
                audio_bitrate=self.audio_bitrate.get_bitrate(),
                output_dir=self.output_dir_widget.get_directory(),
            )
        )


__all__ = [
    "AudioConvertWindow",
]
