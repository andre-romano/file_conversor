
# src\file_conversor\gui\__main__.py
import sys

from types import TracebackType

from PySide6.QtWidgets import QApplication

from file_conversor.config import Log, get_translation
from file_conversor.gui import Environment, MainWindowGUI
from file_conversor.main_helper import MainHelper


LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _global_exception_handler(exc_type: type[BaseException], exc_value: BaseException, exc_traceback: TracebackType | None):
    """
    Captura qualquer erro não tratado e exibe em um popup.
    """
    import traceback

    from PySide6.QtWidgets import QMessageBox

    # format the traceback into a string
    tb_string = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    # print the error to the console (optional, but useful for debugging)
    logger.error(f"{exc_type.__name__}: {exc_value}\n{tb_string}", exc_info=True)

    # avoid showing the popup if the app is running in a non-GUI environment (like CLI or during testing)
    if not QApplication.instance():
        return

    # create a critical error message box to show the error details to the user
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle(_("Critical Error"))
    msg_box.setText(f'{_("Unhandled error occurred:")} {exc_type.__name__}')
    msg_box.setInformativeText(str(exc_value))  # show the error message as the main text in the popup
    msg_box.setDetailedText(tb_string)  # traceback details in the "Show Details" section of the popup
    msg_box.exec()  # show the popup

    sys.exit(1)  # exit the app with an error code


def _start_gui() -> int:
    """ Starts the GUI application. """
    qss_path = Environment.get_gui_folder() / "main.qss"

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Apply the modern cross-platform style
    app.setStyleSheet(qss_path.read_text())  # Load and apply the main stylesheet
    # replace python default exception handler with our custom one to catch unhandled exceptions globally
    sys.excepthook = _global_exception_handler
    window = MainWindowGUI()
    window.show()
    return app.exec()


# Entry point of the app
def main() -> None:
    """ Main entry point for the GUI application. """
    main_helper = MainHelper()
    main_helper.run(_start_gui)


# Start the application
if __name__ == "__main__":
    main()
