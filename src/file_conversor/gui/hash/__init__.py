# src/file_conversor/gui/hash/__init__.py


from file_conversor.config import Environment, get_translation
from file_conversor.gui._widgets import Card, FlowFrame


ICON_PATH = Environment.get_icons_folder()
GUI_PATH = Environment.get_gui_folder()
_ = get_translation()


class HashFrame(FlowFrame):
    def __init__(self) -> None:
        super().__init__()

        self.addItems(
            create_card := Card(
                icon=ICON_PATH / "sha256.ico",
                title=_("Create"),
                description=_("Create a hash (sha256, etc) of files."),
                gui_path=GUI_PATH,
            ),
            check_card := Card(
                icon=ICON_PATH / "check.ico",
                title=_("Check"),
                description=_("Check the hash (sha256, etc) of files."),
                gui_path=GUI_PATH,
            ),
        )
        create_card.clicked.connect(self.on_create_card_clicked)
        check_card.clicked.connect(self.on_check_card_clicked)

    def on_create_card_clicked(self) -> None:
        print("Create card clicked!")

    def on_check_card_clicked(self) -> None:
        print("Check card clicked!")


__all__ = [
    "HashFrame",
]
