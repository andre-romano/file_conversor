
# src\file_conversor\gui\__main__.py
import sys

from PySide6.QtWidgets import QApplication

from file_conversor.gui import MainWindowGUI
from file_conversor.main_helper import MainHelper


# Entry point of the app
def main() -> None:
    """ Main entry point for the GUI application. """

    def _start_gui() -> int:
        """ Starts the GUI application. """
        app = QApplication(sys.argv)
        app.setStyle("Fusion")  # Apply the modern cross-platform style
        window = MainWindowGUI()
        window.show()
        return app.exec()

    main_helper = MainHelper()
    main_helper.run(_start_gui)


# Start the application
if __name__ == "__main__":
    main()
