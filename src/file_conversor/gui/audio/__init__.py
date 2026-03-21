# src/file_conversor/gui/audio/__init__.py

from file_conversor.config import Environment, get_translation
from file_conversor.gui._widgets import Card, FlowFrame


ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()
_ = get_translation()


class AudioFrame(FlowFrame):
    def __init__(self) -> None:
        super().__init__()

        self.addItems(
            convert_card := Card(
                icon=ICON_PATH / "convert.ico",
                title=_("Convert"),
                description=_("Convert to other formats."),
                gui_path=GUI_PATH,
            ),
            info_card := Card(
                icon=ICON_PATH / "info.ico",
                title=_("Info"),
                description=_("Information about the file."),
                gui_path=GUI_PATH,
            ),
            check_card := Card(
                icon=ICON_PATH / "check.ico",
                title=_("Check"),
                description=_("Check the file."),
                gui_path=GUI_PATH,
            ),
        )
        convert_card.clicked.connect(self.on_convert_card_clicked)
        info_card.clicked.connect(self.on_info_card_clicked)
        check_card.clicked.connect(self.on_check_card_clicked)

    def on_convert_card_clicked(self) -> None:
        print("Convert card clicked!")

    def on_info_card_clicked(self) -> None:
        print("Info card clicked!")

    def on_check_card_clicked(self) -> None:
        print("Check card clicked!")


__all__ = [
    "AudioFrame",
]
